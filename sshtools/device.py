#! /usr/bin/python3
"""Classes for managing devices used by other files"""

from __future__ import annotations  # python -3.9 compatibility

import datetime as dt
import json
import socket
from typing import Optional, Union

from timtools.log import get_logger

from sshtools import connection, errors, interface, ip, tools

DEVICES_DIR = tools.CONFIG_DIR / "devices"
logger = get_logger(__name__)


class Device:
    """A physical device"""

    __config_all: dict = None
    __instances: dict[str, "Device"] = {}
    # Config
    hostname: str
    mdns: Optional[str]
    ip_id: int
    config: connection.ConnectionConfig
    ip_address_list_all: ip.IPAddressList
    interfaces: list[interface.Interface]

    last_ip_address: Optional[ip.IPAddress]
    last_ip_address_update: Optional[dt.datetime]

    @classmethod
    def _get_config_all(cls) -> dict[str, dict]:
        """
        Use getter to fix problems with python <3.9 with combined property and classmethod decorators
        TODO: use @property when python >=3.9 can be ensured
        """
        if cls.__config_all is None:
            cls.__config_all = {
                dev.stem: json.load(dev.open("r")) for dev in DEVICES_DIR.iterdir()
            }
        return cls.__config_all

    @classmethod
    def get_devices(cls) -> list[Device]:
        config: dict = cls._get_config_all()
        device_names: list[str] = list(config.keys())
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

        if name not in self._get_config_all().keys() and name != "localhost":
            raise errors.DeviceNotFoundError(name)

        config = self._get_config_all().get(name, {})
        self.hostname = config.get("hostname", name)
        self.ip_id = config.get("ip_id")

        self.config = connection.ConnectionConfig(
            sync=config.get("sync", False),
            ssh=config.get("ssh", True),
            ssh_port=config.get("ssh_port", "22"),
            mosh=config.get("mosh", True),
            user=config.get("user", "tim"),
            priority=config.get("priority", 80),
        )

        if isinstance(self.config.sync, str):
            if self.config.sync.lower() in ["true", "full", "yes"]:
                self.config.sync = True
            elif self.config.sync.lower() in ["false", "no"]:
                self.config.sync = False

        self.interfaces = []
        for iface_data in config.get("interfaces", []):
            iface = interface.Interface(
                self, iface_data.get("name"), iface_data.get("mac", None)
            )
            self.interfaces.append(iface)

        self.ip_address_list_all = ip.IPAddressList()
        for ip_data in config.get("connections", []):
            config_ip_address: Optional[str] = ip_data.get("ip_address", None)
            config_network: connection.Network = connection.Network(
                ip_data.get("network", "public")
            )
            if config_ip_address is not None:
                ip_address = ip.IPAddress(ip_data.get("ip_address"))
            elif config_network.ip_start is not None and self.ip_id is not None:
                ip_address = ip.IPAddress(config_network.ip_start + str(self.ip_id))
            else:
                raise ValueError(
                    f"No IP address configured for {self.name} in network {config_network}"
                )

            ip_address.config = connection.IPConnectionConfig(
                sync=ip_data.get("sync", self.config.sync),
                ssh=ip_data.get("ssh", self.config.ssh),
                ssh_port=ip_data.get("ssh_port", self.config.ssh_port),
                mosh=ip_data.get("mosh", self.config.mosh),
                user=ip_data.get("user", self.config.user),
                priority=ip_data.get("priority", self.config.priority),
                network=config_network,
            )
            self.ip_address_list_all.add(ip_address)

        if self.hostname is not None:
            self.mdns = self.hostname + ".local"
        else:
            self.mdns = None

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
        except errors.DeviceNotFoundError:
            return Device("localhost")

    @property
    def reachable_ip_addresses(self) -> ip.IPAddressList:
        reachable_ips = ip.IPAddressList()
        for ip_address in self.ip_address_list_all:
            if ip_address.config.network.is_connected:
                reachable_ips.add(ip_address)
        return reachable_ips

    def get_ip(self, strict_ip: bool = False) -> ip.IPAddress:
        """
        Returns the IP to used for the device

        :param strict_ip: Only return an actual IP address (no DNS or hostnames allowed)
        """
        if self.is_self():
            if strict_ip:
                return ip.IPAddress("127.0.0.1")
            return ip.IPAddress("localhost")

        if self.reachable_ip_addresses.length() == 0:
            logger.info(f"Found no reachable ips for {self.name}")
            raise errors.DeviceNotPresentError(self.name)

        alive_ips = self.get_active_ips(strict_ip=strict_ip)
        if alive_ips.length() > 0:
            ip_address = alive_ips.get_first()
            logger.info(f"Found ip {ip_address} for {self.name}")
            self.last_ip_address = ip_address
            self.last_ip_address_update = dt.datetime.now()
            return ip_address

        raise errors.NotReachableError(self.name)

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
            possible_ips.add_list(self.reachable_ip_addresses)
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

        logger.info(
            f"Trying {possible_ips.length()} ips for {self.name}: {possible_ips.to_list()}"
        )

        return possible_ips.get_alive_addresses()

    @property
    def ip_address(self) -> ip.IPAddress:
        if self.last_ip_address is not None and self.last_ip_address_update is not None:
            td_update: dt.timedelta = dt.datetime.now() - self.last_ip_address_update
            if td_update.total_seconds() < tools.IP_CACHE_TIMEOUT:
                return self.last_ip_address
        return self.get_ip()

    @property
    def is_super(self) -> bool:
        """Checks whether the device is a super device (aka daily driver)"""
        return self.priority == 0

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
        except (errors.NotReachableError, errors.DeviceNotPresentError):
            return False

    def get_config_value(self, key: str):
        if self.is_present() and self.ip_address.config is not None:
            config = self.ip_address.config
        else:
            config = self.config

        return getattr(config, key)

    @property
    def sync(self) -> Union[str, bool]:
        if self.config.sync is False:
            # If sync is disabled on the device level, don't bother finding the IP
            return self.config.sync

        return self.get_config_value("sync")

    @property
    def user(self) -> str:
        return self.get_config_value("user")

    @property
    def ssh(self) -> bool:
        return self.get_config_value("ssh")

    @property
    def mosh(self) -> bool:
        return self.get_config_value("mosh")

    @property
    def ssh_port(self) -> bool:
        return self.get_config_value("ssh_port")

    @property
    def priority(self) -> int:
        return self.get_config_value("priority")

    def __repr__(self):
        return "<Device({name})>".format(name=self.hostname or self.name)
