import ipaddress
import os
import re

from timtools import bash, log

logger = log.get_logger("sshtools.ip")


class IPAddress:
    ip_address: str
    version: int
    __ip_obj: ipaddress.ip_address

    def __init__(self, ip_address: str):
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

        if self.ip_address.endswith(".local") or self.ip_address in [
            "localhost",
            os.uname().nodename,
        ]:
            logger.debug("%s is a local hostname", self.ip_address)
            return True

        return False

    def is_alive(self) -> bool:
        ping_cmd = [
            "ping",
            "-q",  # be quiet
            "-c 1",  # only try once
        ]
        ping_cmd += [self.ip_address]

        ping_result: bash.CommandResult = bash.run(
            ping_cmd, capture_stdout=True, passable_exit_codes=[0, 2]
        )
        return ping_result.exit_code == 0

    def __repr__(self):
        return f"<sshtools.ip.IPAddress {self.ip_address}>"
