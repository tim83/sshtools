"""Module for handling ip addresses"""
from __future__ import annotations  # python -3.9 compatibility

import dataclasses
import ipaddress
import re
import socket
import subprocess
import typing

import cachetools.func
import timtools.bash
import timtools.log
import timtools.multithreading

import sshtools.connection
import sshtools.device
import sshtools.tools
from sshtools.config import IPConnectionConfig

logger = timtools.log.get_logger("sshtools.ip_address")


@dataclasses.dataclass
class PingResult:
    """Class to store the result of a ping operation"""

    alive: bool
    latency: float


class IPAddress:
    """An IP address. IP objects with the same IP address will behave like singletons"""

    ip_address: str
    version: int
    is_hostname: bool
    config: IPConnectionConfig = None
    __ip_obj: ipaddress.ip_address
    __instances: dict[str, "IPAddress"] = {}

    def __init__(self, ip_address: str, hostname: bool = False):
        if not isinstance(ip_address, str):
            raise ValueError("IP address must by a string.")
        self.ip_address = ip_address
        try:
            self.__ip_obj = ipaddress.ip_address(ip_address)
        except ValueError:
            self.__ip_obj = None
        self.version = self._determine_ip_version()
        self.is_hostname = hostname

    def __new__(cls, ip_address: str, *_, **__):
        if ip_address in cls.__instances:
            return cls.__instances[ip_address]

        instance = super(IPAddress, cls).__new__(cls)
        cls.__instances[ip_address] = instance
        return instance

    @property
    def network(self) -> typing.Optional[sshtools.connection.Network]:
        """The network to which the ip address belongs"""
        if self.config and self.config.network:
            return self.config.network

        for network in sshtools.connection.Network.get_networks():
            if network.has_ip_address(self):
                return network

        return None

    def _determine_ip_version(self) -> int:
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

    @property
    def is_vpn(self) -> bool:
        """Is the ip address a VPN?"""
        return self.network is not None and self.network.is_vpn is True

    def is_local(self, include_vpn: bool = True) -> bool:
        """Is the ip address part a local one?"""
        # https://en.wikipedia.org/wiki/Private_network
        if self.is_vpn:
            return not self.network.is_public and include_vpn

        if self.network and self.network.is_public:
            return True

        if self.__ip_obj and self.__ip_obj.is_private:
            return True

        if self.ip_address.endswith(".local") or self.is_loopback:
            return True

        return False

    @property
    def is_loopback(self) -> bool:
        """Is the ip address a loopback address?"""
        return self.ip_address in [
            "localhost",
            "127.0.0.1",
            "::1",
            socket.gethostname(),
        ]

    def cache_online(self):
        """Call all online/ssh/mosh checks to cache the result"""

        def exec_string_method(method_string: str):
            getattr(self, method_string)()

        timtools.multithreading.mt_map(exec_string_method, ["ping", "sshable"])

    @cachetools.func.ttl_cache(ttl=sshtools.tools.IP_CACHE_TIMEOUT)
    def ping(self) -> PingResult:
        """Is the ip address alive?"""
        if self.config_value("check_online") is False:
            return PingResult(True, -1)

        ping_cmd = [
            "ping",
            "-q",  # be quiet
            "-c 1",  # only try once
        ]
        ping_cmd += [self.ip_address]

        try:
            ping_result: timtools.bash.CommandResult = timtools.bash.run(
                ping_cmd,
                capture_stdout=True,
                capture_stderr=True,
                passable_exit_codes=[0, 2],
                timeout=sshtools.tools.IP_PING_TIMEOUT,
            )
            is_alive = ping_result.exit_code == 0
            if is_alive:
                ping_time = float(
                    ping_result.output.rsplit("\n", maxsplit=1)[-1]
                    .split(" = ")[1]
                    .split("/")[1]
                )
            else:
                ping_time = float("inf")
        except subprocess.TimeoutExpired:
            return PingResult(False, float("inf"))

        return PingResult(is_alive, ping_time)

    @property
    def is_alive(self) -> bool:
        """Returns whether this IP address is alive"""
        return self.ping().alive

    @property
    def latency(self) -> float:
        """Returns the latency of the IP address"""
        return self.ping().latency

    @property
    def ssh_string(self) -> str:
        """Returns the SSH string for this IP ([USER]@[IP])"""
        user: str = self.config_value("user")
        if user is None:
            return self.ip_address
        return f"{user}@{self.ip_address}"

    @cachetools.func.ttl_cache(ttl=sshtools.tools.IP_CACHE_TIMEOUT)
    def is_sshable(self) -> bool:
        """Can an SSH connection be established to the IP?"""
        if not self.is_alive or self.config_value("ssh") is False:
            return False

        ssh_cmd: list[str] = [
            "ssh",
            "-o BatchMode=yes",
            "-o ConnectTimeout=2",
        ]
        if self.config_value("ssh_port") is not None:
            ssh_cmd += [f"-p {self.config_value('ssh_port')}"]
        ssh_cmd += [
            self.ssh_string,
            "exit",
        ]

        try:
            cmd_res = timtools.bash.run(
                ssh_cmd,
                passable_exit_codes=["*"],
                capture_stderr=True,
                capture_stdout=True,
                timeout=sshtools.tools.IP_SSH_TIMEOUT,
            )
            return cmd_res.exit_code == 0
        except subprocess.TimeoutExpired:
            return False

    def __repr__(self):
        return f"<sshtools.ip.IPAddress {self.ip_address}>"

    def __str__(self):
        return self.ip_address

    def config_value(self, key: str):
        """Get the applicable value for a certain configuration key"""
        if self.config is not None:
            return getattr(self.config, key)
        return None
