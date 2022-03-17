#! /usr/bin/python3
"""Classes for managing devices used by other files"""

from __future__ import annotations  # python -3.9 compatibility

import datetime as dt
import json
import socket
from pathlib import Path
from typing import Optional, Union

import timtools.bash
import timtools.locations
import timtools.log

import sshtools.config
import sshtools.connection
import sshtools.errors
import sshtools.interface
import sshtools.ip
import sshtools.pathfinder
import sshtools.tools

DEVICES_DIR = sshtools.tools.CONFIG_DIR / "devices"
logger = timtools.log.get_logger("sshtools.device")


class DeviceConfig:
    """The config for the devices"""

    __config_all: dict = None

    @classmethod
    def _get_config_all(cls) -> dict[str, dict]:
        """
        Use getter to fix problems with python <3.9
        with combined property and classmethod decorators
        TODO: use @property when python >=3.9 can be ensured
        """
        if cls.__config_all is None:
            cls.__config_all = {
                dev.stem: json.load(dev.open("r")) for dev in DEVICES_DIR.iterdir()
            }
        return cls.__config_all

    @classmethod
    def get_config(cls, name) -> dict:
        """
        Return the config of a device
        :param name: The name of the device
        :return: The dictionary containing the config
        """
        config = cls._get_config_all().get(name, {})
        if name not in cls._get_config_all().keys() and name != "localhost":
            raise sshtools.errors.DeviceNotFoundError(name)
        return config

    @classmethod
    def get_devices(cls) -> list[Device]:
        """Return all devices"""
        config: dict = cls._get_config_all()
        device_names: list[str] = list(config.keys())
        return [Device(name) for name in device_names]

    @classmethod
    def get_device(cls, name: str):
        """Return the device with a given name"""
        return Device(cls.get_name_from_hostname(name))

    @classmethod
    def get_name_from_hostname(cls, hostname: str) -> str:
        """
        Returns the name corresponding to a given hostname.
        If no name is found, the hostname is returned
        """
        if hostname in cls._get_config_all().keys():
            return hostname

        for name, config in cls._get_config_all().items():
            if config.get("hostname", None) == hostname:
                return name
        return hostname


class Device:  # pylint:disable=too-many-instance-attributes
    """A physical device"""

    __instances: dict[str, "Device"] = {}

    hostname: str
    mdns: Optional[str]
    ip_id: int
    config: sshtools.config.ConnectionConfig
    ip_address_list_all: sshtools.ip.IPAddressList
    interfaces: list[sshtools.interface.Interface]
    is_main_device: bool

    last_ip_address: Optional[sshtools.ip.IPAddress]
    last_ip_address_update: Optional[dt.datetime]

    def __init__(self, name: str):
        self.last_ip_address = None
        self.last_ip_address_update = None

        name = DeviceConfig.get_name_from_hostname(name)
        config = DeviceConfig.get_config(name)

        self.name = name
        self.hostname = config.get("hostname", name)
        self.ip_id = config.get("ip_id")

        self.config = sshtools.config.ConnectionConfig(
            sync=config.get("sync", False),
            ssh=config.get("ssh", True),
            ssh_port=config.get("ssh_port", "22"),
            mosh=config.get("mosh", True),
            user=config.get("user", "tim"),
            priority=config.get("priority", 80),
        )

        self.is_main_device = config.get("main_device", self.config.sync is not False)

        if isinstance(self.config.sync, str):
            if self.config.sync.lower() in ["true", "full", "yes"]:
                self.config.sync = True
            elif self.config.sync.lower() in ["false", "no"]:
                self.config.sync = False

        self.interfaces = []
        for iface_data in config.get("interfaces", []):
            iface = sshtools.interface.Interface(
                self, iface_data.get("name"), iface_data.get("mac", None)
            )
            self.interfaces.append(iface)

        self.ip_address_list_all = sshtools.ip.IPAddressList()
        for ip_data in config.get("connections", []):
            config_ip_address: Optional[str] = ip_data.get("ip_address", None)
            config_network: sshtools.connection.Network = sshtools.connection.Network(
                ip_data.get("network", "public")
            )
            if config_ip_address is not None:
                ip_address = sshtools.ip.IPAddress(ip_data.get("ip_address"))
            elif config_network.ip_start is not None and self.ip_id is not None:
                ip_address = sshtools.ip.IPAddress(
                    config_network.ip_start + str(self.ip_id)
                )
            else:
                raise ValueError(
                    f"No IP address configured for {self} in network {config_network}"
                )

            ip_address.config = sshtools.ip.IPConnectionConfig(
                sync=ip_data.get("sync", self.config.sync),
                ssh=ip_data.get("ssh", self.config.ssh),
                ssh_port=ip_data.get("ssh_port", self.config.ssh_port),
                mosh=ip_data.get("mosh", self.config.mosh),
                user=ip_data.get("user", self.config.user),
                priority=ip_data.get("priority", self.config.priority),
                network=config_network,
                check_online=ip_data.get("check_online", True),
            )
            self.ip_address_list_all.add(ip_address)

        if self.hostname is not None:
            self.mdns = self.hostname + ".local"
        else:
            self.mdns = None

    def __new__(cls, name: str, *_, **__):
        name = DeviceConfig.get_name_from_hostname(name)
        if name in cls.__instances.keys():
            return cls.__instances[name]

        instance = super(Device, cls).__new__(cls)
        cls.__instances[name] = instance
        return instance

    @staticmethod
    def get_self() -> Device:
        """Return the device object of this machine"""
        hostname = socket.gethostname()
        try:
            return Device(hostname)
        except sshtools.errors.DeviceNotFoundError:
            return Device("localhost")

    @property
    def reachable_ip_addresses(self) -> sshtools.ip.IPAddressList:
        """Returns the reachable ip addresses"""
        reachable_ips = sshtools.ip.IPAddressList()
        for ip_address in self.ip_address_list_all:
            if ip_address.config.network.is_connected:
                reachable_ips.add(ip_address)
        return reachable_ips

    def get_ip(self, strict_ip: bool = False) -> sshtools.ip.IPAddress:
        """
        Returns the IP to used for the device
        :param strict_ip: Only return an actual IP address (no DNS or hostnames allowed)
        """
        if self.is_self:
            if strict_ip:
                return sshtools.ip.IPAddress("127.0.0.1")
            return sshtools.ip.IPAddress(self.hostname)

        if self.reachable_ip_addresses.length == 0:
            logger.info("Found no reachable ips for %s", self)
            raise sshtools.errors.DeviceNotPresentError(self.name)

        alive_ips = self.get_active_ips(strict_ip=strict_ip)
        if alive_ips.length > 0:
            ip_address = alive_ips.first
            logger.info("Found ip %s for %s", ip_address, self)
            self.last_ip_address = ip_address
            self.last_ip_address_update = dt.datetime.now()
            return ip_address

        raise sshtools.errors.NotReachableError(self.name)

    def get_possible_ips(
        self,
        include_dns: bool = True,
        include_hostname: bool = True,
        include_ips: bool = True,
    ) -> sshtools.ip.IPAddressList:
        """Returns all possible IPs that could be reached, within the given parameters"""

        possible_ips: sshtools.ip.IPAddressList = sshtools.ip.IPAddressList()

        def clean_ip_group(
            ip_group: Optional[list[str]],
        ) -> list[sshtools.ip.IPAddress]:
            if ip_group is not None:
                return [
                    sshtools.ip.IPAddress(ipaddr)
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

    def get_active_ips(self, strict_ip: bool = False) -> sshtools.ip.IPAddressList:
        """
        Returns the list of all active ips

        :param strict_ip: Only return an actual IP address (no DNS or hostnames allowed)
        """
        possible_ips: sshtools.ip.IPAddressList
        if strict_ip:
            possible_ips = self.get_possible_ips(
                include_dns=False, include_hostname=False
            )
        else:
            possible_ips = self.get_possible_ips()

        logger.info(
            "Trying %d ips for %s: %s",
            possible_ips.length,
            self,
            possible_ips.to_list(),
        )

        alive_ips = possible_ips.get_alive_addresses()
        logger.info("Found %d IP addresses: %s", alive_ips.length, alive_ips)
        return alive_ips

    @property
    def ip_address(self) -> sshtools.ip.IPAddress:
        """The ip address of this machine"""
        if self.last_ip_address is not None and self.last_ip_address_update is not None:
            td_update: dt.timedelta = dt.datetime.now() - self.last_ip_address_update
            if td_update.total_seconds() < sshtools.tools.IP_CACHE_TIMEOUT:
                return self.last_ip_address
        return self.get_ip()

    @property
    def home(self) -> Path:
        """The home directory of this device"""
        return timtools.locations.get_user_home(self.user)

    @property
    def is_super(self) -> bool:
        """Checks whether the device is a super device (aka daily driver)"""
        return self.priority == 0

    @property
    def is_self(self) -> bool:
        """Checks if the device is the current machine"""
        hostname_machine = socket.gethostname()
        return self.hostname == hostname_machine or self.hostname == "localhost"

    @property
    def is_local(self) -> bool:
        """
        Checks if the device is present on the local LAN (VPN is not regarded as local)
        """
        return self.ip_address.is_local(include_vpn=False)

    @property
    def is_present(self) -> bool:
        """Checks if the device is reachable"""
        try:
            return self.ip_address.is_alive()
        except (
            sshtools.errors.NotReachableError,
            sshtools.errors.DeviceNotPresentError,
        ):
            return False

    @property
    def is_sshable(self) -> bool:
        """Checks whether a device is reachable and can receive an SSH-connection"""
        if self.is_present and self.ssh:
            cmd_res = timtools.bash.run(
                [
                    "ssh",
                    "-o BatchMode=yes",
                    "-o ConnectTimeout=2",
                    f"-p {self.ssh_port}",
                    f"{self.user}@{self.ip_address}",
                    "exit",
                ],
                passable_exit_codes=["*"],
                capture_stderr=True,
                capture_stdout=True,
            )
            return cmd_res.exit_code == 0
        return False

    def _get_config_value(self, key: str):
        """Get the applicable value for a certain configuration key"""
        if self.is_present and self.ip_address.config is not None:
            config = self.ip_address.config
        else:
            config = self.config

        return getattr(config, key)

    def can_connect_to_device(self, target: "Device") -> bool:
        """Can this device connect to the target device"""
        return sshtools.pathfinder.Path.device_is_present_for_device(self, target)

    @property
    def sync(self) -> Union[str, bool]:
        """Can the device be used for sync?"""
        if self.config.sync is False:
            # If sync is disabled on the device level, don't bother finding the IP
            return self.config.sync

        return self._get_config_value("sync")

    @property
    def user(self) -> str:
        """What is the user to connect to on this device?"""
        return self._get_config_value("user")

    @property
    def ssh(self) -> bool:
        """Can SSH be used on this device?"""
        return self._get_config_value("ssh")

    @property
    def mosh(self) -> bool:
        """Can MOSH be used on this device?"""
        return self._get_config_value("mosh")

    @property
    def ssh_port(self) -> bool:
        """What port should be used for SSH?"""
        return self._get_config_value("ssh_port")

    @property
    def priority(self) -> int:
        """What is the priority of this device?"""
        return self._get_config_value("priority")

    def __repr__(self):
        return "<Device({name})>".format(name=self.hostname or self.name)

    def __str__(self):
        return self.hostname or self.name
