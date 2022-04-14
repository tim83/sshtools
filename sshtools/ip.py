"""Module for handling collections of IP address"""
from __future__ import annotations

import socket
from typing import Union

import psutil
import timtools.log
from cachetools.func import ttl_cache

import sshtools.errors
import sshtools.ip_address
import sshtools.tools

logger = timtools.log.get_logger("sshtools.ip")

IPConnectionConfig = sshtools.ip_address.IPConnectionConfig
IPAddress = sshtools.ip_address.IPAddress


class IPAddressList:
    """A collection of IPAddress"""

    _ip_addresses: list[IPAddress]

    def __init__(self, ip_addresses: list[IPAddress] = None):
        if ip_addresses is not None:
            self._ip_addresses = ip_addresses.copy()
        else:
            self._ip_addresses = []

    def add(self, ip_address: IPAddress):
        """
        Add an ip address to the collection
        :param ip_address: The IPAddress to add
        """
        if isinstance(ip_address, IPAddress):
            self._ip_addresses.append(ip_address)
        else:
            raise ValueError("Only IPAddress objects can be added to a IPAddressList")

    def add_list(self, ip_addresses: Union[list[IPAddress], "IPAddressList"]):
        """
        Add a list of ip address to the collection
        :param ip_addresses: A list of IPAddress or a IPAddressList object to add
        """
        if all(isinstance(ip, IPAddress) for ip in ip_addresses):
            self._ip_addresses += ip_addresses
        else:
            raise ValueError("Only IPAddress objects can be added to a IPAddressList")

    def get_alive_addresses(self) -> "IPAddressList":
        """
        Determine which ip addresses from the collection are reachable
        :return: A IPAddressList of reachable ip addresses
        """
        alive_ips_list = sshtools.tools.mt_filter(
            lambda i: i.is_alive(), self._ip_addresses
        )
        alive_ips: IPAddressList = IPAddressList(alive_ips_list)
        return alive_ips

    def sort_ips(self):
        """
        Sort the ip addresses based on the order of precedence for connecting
        """
        sorted_ips = {}

        def sort_list(ip_list):
            return sorted(ip_list, key=str)

        # Loopback
        sorted_ips.update(
            dict.fromkeys(
                sort_list(filter(lambda ip: ip.is_loopback, self._ip_addresses))
            )
        )
        # mDNS
        sorted_ips.update(
            dict.fromkeys(
                sort_list(
                    filter(lambda ip: str(ip).endswith(".local"), self._ip_addresses)
                )
            )
        )
        # Local IPs
        sorted_ips.update(
            dict.fromkeys(
                sort_list(
                    filter(
                        lambda ip: ip.is_local(include_vpn=False), self._ip_addresses
                    )
                )
            )
        )
        # Zerotier IPs
        sorted_ips.update(
            dict.fromkeys(
                sort_list(
                    filter(lambda ip: ip.is_local(include_vpn=True), self._ip_addresses)
                )
            )
        )
        # Rest
        sorted_ips.update(dict.fromkeys(sort_list(self._ip_addresses)))
        self._ip_addresses: list[str] = list(sorted_ips.keys())

    @property
    def first(self) -> IPAddress:
        """Returns the first ip address in the collection after sorting"""
        self.sort_ips()
        return self._ip_addresses[0]

    @property
    def length(self) -> int:
        """Returns the length of the collection"""
        return len(self._ip_addresses)

    @property
    def list(self) -> list[IPAddress]:
        """Returns a list object of the collections"""
        return self._ip_addresses

    def __iter__(self):
        """Enables iterating over the list"""
        return IPAddressListIterator(self)


class IPAddressListIterator:  # pylint: disable=too-few-public-methods
    """Iterator class for IPAddressLists"""

    def __init__(self, ip_address_list: IPAddressList):
        self._ip_address_list = ip_address_list
        # variable to keep track of current index
        self._index = 0

    def __next__(self):
        """Returns the next value from the object's lists"""
        if self._index < self._ip_address_list.length:
            result = self._ip_address_list.list[self._index]
            self._index += 1
            return result

        raise StopIteration


@ttl_cache(ttl=3)
def get_current_ips() -> IPAddressList:
    """Get the IPs that the current device has assigned"""
    interface_data = psutil.net_if_addrs()
    interface_names = sorted(interface_data.keys())
    addresses = IPAddressList()
    for interface_name in interface_names:
        try:
            ip_address_list = IPAddressList(
                [
                    sshtools.ip.IPAddress(address.address)
                    for address in interface_data[interface_name]
                    if address.family == socket.AF_INET
                ]
            )
            addresses.add_list(ip_address_list)
        except StopIteration:
            pass
    if addresses.length == 0:
        raise sshtools.errors.NetworkError()

    logger.debug(
        "This machine has %d ip addresses: %s",
        addresses.length,
        str(addresses.list),
    )

    return addresses
