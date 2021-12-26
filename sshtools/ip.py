import concurrent.futures
import ipaddress
import re
import socket

import cachetools.func
from timtools import bash, log

logger = log.get_logger("sshtools.ip")


class IPAddress:
    ip_address: str
    version: int
    __ip_obj: ipaddress.ip_address

    def __init__(self, ip_address: str):
        if type(ip_address) != str:
            raise ValueError("IP address must by a string.")
        self.ip_address = ip_address
        try:
            self.__ip_obj = ipaddress.ip_address(ip_address)
        except ValueError:
            self.__ip_obj = None
        self.version = self._determine_version()

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

        if self.ip_address.startswith("192.168.193"):
            logger.debug("%s is a VPN connection", self.ip_address)
            return include_vpn

        if self.__ip_obj and self.__ip_obj.is_private:
            logger.debug("%s is private", self.ip_address)
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

    @cachetools.func.ttl_cache(ttl=3)  # cache value for 3 seconds
    def is_alive(self) -> bool:
        ping_cmd = [
            "ping",
            "-q",  # be quiet
            "-c 1",  # only try once
        ]
        ping_cmd += [self.ip_address]

        ping_result: bash.CommandResult = bash.run(
            ping_cmd,
            capture_stdout=True,
            capture_stderr=True,
            passable_exit_codes=[0, 2],
        )
        return ping_result.exit_code == 0

    def __repr__(self):
        return f"<sshtools.ip.IPAddress {self.ip_address}>"

    def __str__(self):
        return self.ip_address


class IPAddressList:
    _ip_addresses: list[IPAddress]

    def __init__(self, ip_addresses: list[IPAddress] = None):
        if ip_addresses is not None:
            self._ip_addresses = ip_addresses
        else:
            self._ip_addresses = []

    def add(self, ip_address: IPAddress):
        self._ip_addresses.append(ip_address)

    def add_list(self, ip_addresses: list[IPAddress]):
        self._ip_addresses += ip_addresses

    def get_alive_addresses(self) -> "IPAddressList":
        alive_ips: IPAddressList = IPAddressList()

        def check_ip_alive(ip_address: IPAddress):
            if ip_address.is_alive():
                alive_ips.add(ip_address)

        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            executor.map(check_ip_alive, self._ip_addresses)

        return alive_ips

    def sort_ips(self):
        sorted_ips = {}
        # Loopback
        sorted_ips.update(
            dict.fromkeys(filter(lambda ip: ip.is_loopback(), self._ip_addresses))
        )
        # mDNS
        sorted_ips.update(
            dict.fromkeys(
                filter(lambda ip: str(ip).endswith(".local"), self._ip_addresses)
            )
        )
        # Local IPs
        sorted_ips.update(
            dict.fromkeys(
                filter(lambda ip: ip.is_local(include_vpn=False), self._ip_addresses)
            )
        )
        # Zerotier IPs
        sorted_ips.update(
            dict.fromkeys(
                filter(lambda ip: ip.is_local(include_vpn=True), self._ip_addresses)
            )
        )
        # Rest
        sorted_ips.update(
            dict.fromkeys(sorted(self._ip_addresses, key=lambda ip: str(ip)))
        )
        self._ip_addresses: list[str] = list(sorted_ips.keys())

    def get_first(self) -> IPAddress:
        self.sort_ips()
        return self._ip_addresses[0]

    def length(self) -> int:
        return len(self._ip_addresses)
