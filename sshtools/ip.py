"""Module for handling collections of IP address"""
from __future__ import annotations

import socket
from typing import Union

import psutil
import timtools.log
import timtools.multithreading
from cachetools.func import ttl_cache

import sshtools.errors
import sshtools.ip_address
import sshtools.tools

logger = timtools.log.get_logger("sshtools.ip")

IPConnectionConfig = sshtools.ip_address.IPConnectionConfig
IPAddress = sshtools.ip_address.IPAddress


def hash_ip_list(ip_list: list[IPAddress]) -> int:
    """Return a unique hash for a list of IPAddresses"""
    ip_str_list: list[str] = [str(ip_address) for ip_address in ip_list]
    return hash(",".join(ip_str_list))


class IPAddressList:
    """A collection of IPAddress"""

    _ip_addresses: list[IPAddress]
    _last_sort_hash: int

    def __init__(self, ip_addresses: list[IPAddress] = None):
        if ip_addresses is not None:
            self._ip_addresses = ip_addresses.copy()
        else:
            self._ip_addresses = []
        self._last_sort_hash = 0

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

    def get_alive_addresses(self, only_sshable: bool = False) -> "IPAddressList":
        """
        Determine which ip addresses from the collection are reachable.
        Multiple filters (only_*) will act as an AND operation.

        :param only_sshable: Only return IPs that can be connected to using SSH

        :return: A IPAddressList of reachable ip addresses
        """

        def is_ip_alive(ip_address: IPAddress) -> bool:
            out = ip_address.is_alive
            if only_sshable:
                out = out and ip_address.is_sshable()
            return out

        # Lookup ssh/mosh-ability for all IPAddresses simultaneously to improve performance
        timtools.multithreading.mt_map(lambda i: i.cache_online, self._ip_addresses)

        alive_ips_list = sshtools.tools.mt_filter(is_ip_alive, self._ip_addresses)
        alive_ips: IPAddressList = IPAddressList(alive_ips_list)
        return alive_ips

    def sort_ips(self):
        """
        Sort the ip addresses based on the order of precedence for connecting
        """
        if self._is_sorted:
            return

        def sort_value(ip_address: IPAddress) -> float:
            value: float = ip_address.latency
            if not any(char.isdigit() for char in str(ip_address)):
                if ".local" in str(ip_address):
                    value -= 7
                else:
                    value -= 5

            if (ip_address.config is not None) and (not ip_address.config.mosh):
                value += 15

            return value

        sorted_ips = {}

        # Lookup ssh/mosh-ability for all IPAddresses simultaneously to improve performance
        timtools.multithreading.mt_map(lambda i: i.cache_online, self._ip_addresses)

        sorted_ips.update(
            dict.fromkeys(
                sorted(
                    self._ip_addresses,
                    key=sort_value,
                )
            )
        )
        self._ip_addresses = list(sorted_ips.keys())
        self._last_sort_hash = hash_ip_list(self._ip_addresses)

    @property
    def _is_sorted(self):
        """
        Checks if the order and/or composition of the ip list
        has been changed since the last sort
        """
        list_hash = hash_ip_list(self._ip_addresses)
        return list_hash == self._last_sort_hash

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
