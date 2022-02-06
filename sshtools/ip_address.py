from __future__ import annotations  # python -3.9 compatibility

import ipaddress
import re
import socket
import subprocess
import typing

import cachetools.func
from timtools import bash, log

import sshtools.connection
import sshtools.device
from sshtools import tools
from sshtools.config import IPConnectionConfig

logger = log.get_logger("sshtools.ip_address")


class IPAddress:
    """An IP address. IP objects with the same IP address will behave like singletons"""

    ip_address: str
    version: int
    config: IPConnectionConfig = None
    __ip_obj: ipaddress.ip_address
    __instances: dict[str, "IPAddress"] = {}

    def __init__(self, ip_address: str):
        if type(ip_address) != str:
            raise ValueError("IP address must by a string.")
        self.ip_address = ip_address
        try:
            self.__ip_obj = ipaddress.ip_address(ip_address)
        except ValueError:
            self.__ip_obj = None
        self.version = self._determine_version()

    def __new__(cls, ip_address: str, *args, **kwargs):
        if ip_address in cls.__instances.keys():
            return cls.__instances[ip_address]

        instance = super(IPAddress, cls).__new__(cls)
        cls.__instances[ip_address] = instance
        return instance

    @property
    def network(self) -> typing.Optional[sshtools.connection.Network]:
        if self.config and self.config.network:
            return self.config.network

        for network in sshtools.connection.Network.get_networks():
            if network.has_ip_address(self):
                return network

        return None

    def _determine_version(self) -> int:
        """
        Determines the version of the IP address (IPv4 or IPv6)
        :return: The version number of the IP standard
        """
        if self.__ip_obj:
            return self.__ip_obj.version

        if re.match(
            r"^([a-zA-Z0-9](?:(?:[a-zA-Z0-9-]*|(?<!-)\.(?![-.]))*[a-zA-Z0-9]+)?)$",
            self.ip_address,
        ):
            return 0

        raise ValueError(f"{self.ip_address} is not a valid ip address or hostname.")

    def is_local(self, include_vpn: bool = True) -> bool:
        # https://en.wikipedia.org/wiki/Private_network

        if self.network and self.network.is_vpn is True:
            if self.network.is_public is True:
                logger.debug("%s is public VPN connection", self.ip_address)
                return False
            logger.debug("%s is a VPN connection", self.ip_address)
            return include_vpn

        if self.__ip_obj and self.__ip_obj.is_private:
            logger.debug("%s is private connection", self.ip_address)
            return True

        if self.ip_address.endswith(".local") or self.is_loopback():
            logger.debug("%s is a local hostname", self.ip_address)
            return True

        return False

    def is_loopback(self) -> bool:
        return self.ip_address in [
            "localhost",
            "127.0.0.1",
            "::1",
            socket.gethostname(),
        ]

    @cachetools.func.ttl_cache(ttl=tools.IP_CACHE_TIMEOUT)
    def is_alive(self) -> bool:
        if self.config and not self.config.check_online:
            return True

        ping_cmd = [
            "ping",
            "-q",  # be quiet
            "-c 1",  # only try once
        ]
        ping_cmd += [self.ip_address]

        try:
            ping_result: bash.CommandResult = bash.run(
                ping_cmd,
                capture_stdout=True,
                capture_stderr=True,
                passable_exit_codes=[0, 2],
                timeout=0.7,
            )
        except subprocess.TimeoutExpired:
            return False

        return ping_result.exit_code == 0

    def __repr__(self):
        return f"<sshtools.ip.IPAddress {self.ip_address}>"

    def __str__(self):
        return self.ip_address
