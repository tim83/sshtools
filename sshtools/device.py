#! /usr/bin/python3
"""Classes for managing devices used by other files"""

from __future__ import annotations  # python -3.9 compatibility

import datetime as dt
import json
import socket
from pathlib import Path
from typing import Optional, Union

import psutil
from timtools.log import get_logger

import sshtools.errors
from sshtools import ip
from sshtools.errors import (
    DeviceNotFoundError,
    DeviceNotPresentError,
    NetworkError,
    NotReachableError,
)

project_dir = Path(__file__).parent
config_dir = project_dir.parent / "config"
devices_dir = config_dir / "devices"
logger = get_logger(__name__)


def get_current_ips() -> ip.IPAddressList:
    """Get the IPs that the current device has assigned"""
    interface_data = psutil.net_if_addrs()
    interface_names = sorted(interface_data.keys())
    addresses = ip.IPAddressList()
    logger.debug(f"Networkinterfaces: {interface_names}")
    for interface_name in interface_names:
        try:
            if interface_name[:3] in ["eth", "wla", "enp", "wlo", "wlp", "eno"]:
                ip_addr = ip.IPAddress(
                    next(
                        address.address
                        for address in interface_data[interface_name]
                        if address.family == socket.AF_INET
                    )
                )
                addresses.add(ip_addr)
        except StopIteration:
            pass
    if addresses.length() == 0:
        raise NetworkError()
    else:
        logger.debug("Found %s  ips for this machine.", addresses.length())

    return addresses


def get_networks() -> list[str]:
    """Get the IPs that the networks the current machine has access to"""
    networks: list[str] = []

    ips = get_current_ips()
    interfaces = sorted(psutil.net_if_addrs().keys())

    def check_start_ip(ip_list: ip.IPAddressList, start: str) -> bool:
        return any(str(ip_address).startswith(start) for ip_address in ip_list)

    if check_start_ip(ips, "192.168.23") or "tun0" in interfaces:
        # own kot network
        logger.info("Detected Tims Kot network.")
        networks.append("kot-tim")
    if check_start_ip(ips, "192.168.20"):
        # Home network
        logger.info("Detected Home network.")
        networks.append("home")
    if check_start_ip(ips, "192.168.24"):
        # Own home network
        logger.info("Detected Tims Home network.")
        networks.append("home-tim")
    if check_start_ip(ips, "192.168.193") or "ztuga6wg3j" in interfaces:
        logger.info("Detected ZeroTier One VPN")
        networks.append("zerotier")

    return networks


class Device:
    """A physical device"""

    __config_all: dict = None
    __instances: dict[str, "Device"] = {}
    # Config
    hostname: str
    sync: Union[bool, str]
    ssh: bool
    ssh_port: int
    mosh: bool
    user: str
    mdns: Optional[str]
    ip_address_list: ip.IPAddressList
    ip_address_list_all: ip.IPAddressList

    last_ip_address: Optional[ip.IPAddress]
    last_ip_address_update: Optional[dt.datetime]

    @classmethod
    @property
    def _config_all(cls) -> dict:
        if Device.__config_all is None:
            Device.__config_all = {
                dev.stem: json.load(dev.open("r")) for dev in devices_dir.iterdir()
            }
        return Device.__config_all

    @classmethod
    def get_devices(cls) -> list[Device]:
        device_names: list[str] = cls._config_all.keys()
        return [Device(name) for name in device_names]

    @staticmethod
    def get_device(name: str):
        if name in Device.__instances.keys():
            return Device.__instances.get(name)

        return Device(name)

    def __init__(self, name: str):
        self.name = name
        self.last_ip_address = None
        self.last_ip_address_update = None

        if name not in self._config_all.keys() and name != "localhost":
            raise DeviceNotFoundError(name)

        config = self._config_all.get(name, {})
        self.hostname = config.get("hostname", name)
        self.sync = config.get("sync", False)
        self.ssh = config.get("ssh", True)
        self.ssh_port = config.get("ssh_port", "22")
        self.mosh = config.get("mosh", True)
        self.user = config.get("user", "tim")

        current_networks = get_networks()
        self.ip_address_list = ip.IPAddressList()
        self.ip_address_list_all = ip.IPAddressList()
        for ip_data in config.get("connections", []):
            ip_address = ip.IPAddress(ip_data.get("ip_address"))
            self.ip_address_list_all.add(ip_address)
            if ip_data.get("network", "") in current_networks:
                self.ip_address_list.add(ip_address)

        if self.hostname is not None:
            self.mdns = self.hostname + ".local"
        else:
            self.mdns = None

        if isinstance(self.sync, str):
            if self.sync.lower() in ["true", "full", "yes"]:
                self.sync = True
            elif self.sync.lower() in ["false", "no"]:
                self.sync = False

    def __new__(cls, name: str, *args, **kwargs):
        if name in cls.__instances.keys():
            return cls.__instances[name]

        instance = super(Device, cls).__new__(cls)
        cls.__instances[name] = instance
        return instance

    @staticmethod
    def get_self() -> Device:
        hostname = socket.gethostname()
        try:
            return Device(hostname.rstrip("-tim"))
        except DeviceNotFoundError:
            return Device("localhost")

    def get_ip(self, strict_ip: bool = False) -> ip.IPAddress:
        """
        Returns the IP to used for the device
        :param strict_ip: Only return an actual IP address (no DNS or hostnames allowed)
        """
        if self.is_self():
            if strict_ip:
                return ip.IPAddress("127.0.0.1")
            return ip.IPAddress("localhost")

        if self.ip_address_list.length() == 0:
            raise DeviceNotPresentError(self.name)

        alive_ips = self.get_active_ips(strict_ip=strict_ip)
        if alive_ips.length() > 0:
            ip_address = alive_ips.get_first()
            logger.info(f"Found ip {ip_address} for {self.name}")
            self.last_ip_address = ip_address
            self.last_ip_address_update = dt.datetime.now()
            return ip_address

        raise NotReachableError(self.name)

    def get_possible_ips(
        self,
        include_dns: bool = True,
        include_hostname: bool = True,
        include_ips: bool = True,
    ) -> ip.IPAddressList:
        """Returns all possible IPs that could be reached, within the given parameters"""

        possible_ips: ip.IPAddressList = ip.IPAddressList()

        def clean_ip_group(ip_group: Optional[list[str]]) -> list[ip.IPAddress]:
            if ip_group is not None:
                return [
                    ip.IPAddress(ipaddr)
                    for ipaddr in ip_group
                    if ipaddr is not None and ipaddr not in [""]
                ]
            return []

        if include_ips:
            possible_ips.add_list(self.ip_address_list)
        if include_dns:
            possible_ips.add_list(clean_ip_group([self.mdns]))
        if include_hostname:
            possible_ips.add_list(clean_ip_group([self.hostname]))

        return possible_ips

    def get_active_ips(self, strict_ip: bool = False) -> ip.IPAddressList:
        """
        Returns the list of all active ips
        :param strict_ip: Only return an actual IP address (no DNS or hostnames allowed)
        """
        possible_ips: ip.IPAddressList
        if strict_ip:
            possible_ips = self.get_possible_ips(
                include_dns=False, include_hostname=False
            )
        else:
            possible_ips = self.get_possible_ips()

        return possible_ips.get_alive_addresses()

    @property
    def ip_address(self) -> ip.IPAddress:
        if self.last_ip_address is not None and self.last_ip_address_update is not None:
            td_update: dt.timedelta = dt.datetime.now() - self.last_ip_address_update
            if td_update < dt.timedelta(seconds=30):
                return self.last_ip_address
        return self.get_ip()

    def is_self(self) -> bool:
        """Checks if the device is the current machine"""
        hostname_machine = socket.gethostname()
        return self.hostname == hostname_machine or self.hostname == "localhost"

    def is_local(self, include_vpn: bool = True) -> bool:
        """
        Checks if the device is present on the local LAN
        :param include_vpn: Does a VPN (e.g. zerotier) count as part of the LAN?
        """
        return self.ip_address.is_local(include_vpn=include_vpn)

    def is_present(self) -> bool:
        """Checks if the device is reachable"""
        try:
            return self.ip_address.is_alive()
        except sshtools.errors.NotReachableError:
            return False

    def __repr__(self):
        return "<Device({name})>".format(name=self.hostname or self.name)
