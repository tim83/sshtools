#! /usr/bin/python3
"""Classes for managing devices used by other files"""

from __future__ import annotations  # python -3.9 compatibility

import datetime as dt
import os
import socket
import subprocess
from collections import OrderedDict
from configparser import ConfigParser, NoSectionError, RawConfigParser
from os.path import dirname, expanduser, join
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

project_dir = dirname(__file__)
logger = get_logger(__name__)


def get_ips() -> ip.IPAddressList:
    """Get the IPs that the current device has assigned"""
    interfaces = psutil.net_if_addrs()
    interface_names = sorted(interfaces.keys())
    addresses = ip.IPAddressList()
    logger.debug(f"Networkinterfaces: {interface_names}")
    for interface_name in interface_names:
        try:
            if interface_name[:3] in ["eth", "wla", "enp", "wlo", "wlp", "eno"]:
                ip_addr = ip.IPAddress(
                    next(
                        address.address
                        for address in interfaces[interface_name]
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


class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if (
            isinstance(value, list)
            and key in self
            and key in ["eth", "wlan", "emac", "wmac"]
        ):
            self[key].extend(value)
        else:
            super(OrderedDict, self).__setitem__(key, value)


class Device:  # pylint: disable=too-many-instance-attributes
    """A physical device"""

    config: ConfigParser = None
    config_all: ConfigParser = None
    devices: list = None
    current_ips: ip.IPAddressList = get_ips()
    # Config
    hostname: str
    wlan: Union[str, list[str]]
    eth: Union[str, list[str]]
    present: bool
    sync: bool
    ssh: Union[str, bool]
    ssh_port: int
    mosh: bool
    emac: str
    wmac: str
    user: str
    relay: str
    relay_to: str
    mdns: Optional[str]

    last_ip_addr: Optional[ip.IPAddress]
    last_ip_addr_update: Optional[dt.datetime]

    unique_devices: dict[str, "Device"] = dict()

    @staticmethod
    def get_device_names(extra_config=None):
        """Returns and stores the configured devices"""
        if not extra_config:
            extra_config = []

        general_devices_config: str = join(project_dir, "devices.ini")
        local_devices_config: str = expanduser("~/sshtools/devices.ini")
        config_files = [general_devices_config, local_devices_config] + extra_config

        try:
            ssid = subprocess.check_output(["iwgetid", "-r"]).decode().strip("\n")
            if "WiFi-Home" in ssid:
                config_files.append(join(project_dir, "home.ini"))
            elif "Predikerinnenstraat 10" in ssid:
                config_files.append(join(project_dir, "kot.ini"))
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.debug("WiFi not connected")

        ips = Device.current_ips
        ifaces = sorted(psutil.net_if_addrs().keys())
        # Give priority to my own routers (192.168.{23,24}.*) over the home routers (
        # 192.168.20.*)
        ip_id = str(ips.get_first())[:10]
        if ip_id in ["192.168.23"] or "tun0" in ifaces:
            # own kot network
            logger.info("Detected Tims Kot network.")
            config_files.append(join(project_dir, "kot-tim.ini"))
        if ip_id in ["192.168.20"]:
            # Home network
            logger.info("Detected Home network.")
            config_files.append(join(project_dir, "home.ini"))
        if ip_id in ["192.168.24"]:
            # Own home network
            logger.info("Detected Tims Home network.")
            config_files.append(join(project_dir, "home-tim.ini"))
        if ip_id in ["192.168.193"] or "ztuga6wg3j" in ifaces:
            logger.info("Detected ZeroTier One VPN")
            config_files.append(join(project_dir, "zerotier.ini"))

        Device.config_all = RawConfigParser(dict_type=MultiOrderedDict, strict=False)
        Device.config = ConfigParser(strict=False)
        for config in [Device.config_all, Device.config]:
            config.read(config_files)
        Device.devices = Device.config.sections()

        return Device.devices

    @staticmethod
    def get_device(name: str, verbose: bool = False):
        if name in Device.unique_devices.keys():
            return Device.unique_devices[name]

        return Device(name, verbose)

    def __init__(self, name: str, verbose: bool = False):
        self.logger = get_logger("ssh-tool.devices", verbose=verbose)
        if name not in Device.unique_devices.keys():
            Device.unique_devices[name] = self
        else:
            raise ValueError("A device object for this machine already exists")

        self.name = name
        self.get_config(name)
        self.last_ip_addr = None
        self.last_ip_addr_update = None

    def get_config(self, name, relay=None):
        """Loads and stores the device's config"""
        if relay:
            self.get_device_names(extra_config=[expanduser(relay.relay_to)])
        elif not self.config:
            self.get_device_names()

        try:
            self.hostname = self.config.get(name, "hostname", fallback=None)
            self.wlan = self.config_all.get(name, "wlan", fallback=None)
            self.eth = self.config_all.get(name, "eth", fallback=None)
            self.present = self.wlan is not None or self.eth is not None
            self.sync = self.config.get(name, "sync", fallback=True)
            self.ssh = self.config.getboolean(name, "ssh", fallback=True)
            self.ssh_port = self.config.get(name, "ssh_port", fallback=22)
            self.mosh = self.config.getboolean(name, "mosh", fallback=False)
            self.emac = self.config.get(name, "emac", fallback=None)
            self.wmac = self.config.get(name, "wmac", fallback=None)
            self.user = self.config.get(name, "user", fallback="tim")
            self.relay = self.config.get(name, "relay", fallback=None)
            self.relay_to = self.config.get(name, "relay_to", fallback=None)
            if self.hostname is not None:
                self.mdns = self.hostname + ".local"
            else:
                self.mdns = None
            if isinstance(self.sync, str):
                if self.sync == "True":
                    self.sync = True
                elif self.sync == "False":
                    self.sync = False
        except NoSectionError as error:
            raise DeviceNotFoundError(name) from error

    def get_ip(self, strict_ip: bool = False) -> ip.IPAddress:
        """
        Returns the IP to used for the device
        :param strict_ip: Only return an actual IP address (no DNS or hostnames allowed)
        """
        if not self.eth and not self.wlan:
            raise DeviceNotPresentError(self.name)

        if self.hostname == socket.gethostname():
            return ip.IPAddress(self.hostname)

        alive_ips = self.get_active_ips(strict_ip=strict_ip)
        if alive_ips.length() > 0:
            ip_addr = alive_ips.get_first()
            logger.info(f"Found ip {ip_addr} for {self.name}")
            self.last_ip_addr = ip_addr
            self.last_ip_addr_update = dt.datetime.now()
            return ip_addr

        raise NotReachableError(self.name)

    def get_possible_ips(
        self,
        include_dns: bool = True,
        include_hostname: bool = True,
        include_eth: bool = True,
        include_wlan: bool = True,
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

        if include_eth:
            possible_ips.add_list(clean_ip_group(self.eth))
        if include_wlan:
            possible_ips.add_list(clean_ip_group(self.wlan))
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
        if self.last_ip_addr is not None and self.last_ip_addr_update is not None:
            td_update: dt.timedelta = dt.datetime.now() - self.last_ip_addr_update
            if td_update < dt.timedelta(seconds=30):
                return self.last_ip_addr
        return self.get_ip()

    def get_relay(self):
        """Return the relay device to be used when connecting to this device"""
        if self.relay:
            return Device.get_device(self.relay)
        return None

    def is_self(self) -> bool:
        """Checks if the device is the current machine"""
        hostname_machine = os.uname().nodename
        return self.hostname == hostname_machine

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
