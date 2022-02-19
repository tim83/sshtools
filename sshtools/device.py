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
import sshtools.tools

DEVICES_DIR = sshtools.tools.CONFIG_DIR / "devices"
logger = timtools.log.get_logger("sshtools.device")


class Device:
    """A physical device"""

    __config_all: dict = None
    __instances: dict[str, "Device"] = {}
    # Config
    hostname: str
    mdns: Optional[str]
    ip_id: int
    config: sshtools.config.ConnectionConfig
    ip_address_list_all: sshtools.ip.IPAddressList
    interfaces: list[sshtools.interface.Interface]
    is_main_device: bool

    last_ip_address: Optional[sshtools.ip.IPAddress]
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
            raise sshtools.errors.DeviceNotFoundError(name)

        config = self._get_config_all().get(name, {})
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
                    f"No IP address configured for {self.name} in network {config_network}"
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
        except sshtools.errors.DeviceNotFoundError:
            return Device("localhost")

    @property
    def reachable_ip_addresses(self) -> sshtools.ip.IPAddressList:
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
        if self.is_self():
            if strict_ip:
                return sshtools.ip.IPAddress("127.0.0.1")
            return sshtools.ip.IPAddress("localhost")

        if self.reachable_ip_addresses.length() == 0:
            logger.info(f"Found no reachable ips for {self.name}")
            raise sshtools.errors.DeviceNotPresentError(self.name)

        alive_ips = self.get_active_ips(strict_ip=strict_ip)
        if alive_ips.length() > 0:
            ip_address = alive_ips.get_first()
            logger.info(f"Found ip {ip_address} for {self.name}")
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
            f"Trying {possible_ips.length()} ips for {self.name}: {possible_ips.to_list()}"
        )

        alive_ips = possible_ips.get_alive_addresses()
        logger.info(f"Found {alive_ips.length()} IP addresses: {alive_ips}")
        return alive_ips

    @property
    def ip_address(self) -> sshtools.ip.IPAddress:
        if self.last_ip_address is not None and self.last_ip_address_update is not None:
            td_update: dt.timedelta = dt.datetime.now() - self.last_ip_address_update
            if td_update.total_seconds() < sshtools.tools.IP_CACHE_TIMEOUT:
                return self.last_ip_address
        return self.get_ip()

    @property
    def home(self) -> Path:
        return timtools.locations.get_user_home(self.user)

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
        except (
            sshtools.errors.NotReachableError,
            sshtools.errors.DeviceNotPresentError,
        ):
            return False

    def is_sshable(self) -> bool:
        """Checks whether a device is reachable and can receive an SSH-connection"""
        if self.is_present() and self.ssh:
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
