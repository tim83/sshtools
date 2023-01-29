"""Module for handling networks"""
from __future__ import annotations  # python -3.9 compatibility

import json
import typing
from pathlib import Path

import psutil
import timtools.log

import sshtools.errors
import sshtools.interface
import sshtools.ip
import sshtools.tools

if typing.TYPE_CHECKING:
    import sshtools.device

logger = timtools.log.get_logger("sshtools.connection")

NETWORK_DIR: Path = sshtools.tools.CONFIG_DIR / "networks"


class Network:
    """A network"""

    __instances: dict[str, Network] = {}
    __config_all: dict[str, dict] = {}
    name: str
    is_vpn: bool
    is_public: bool
    ip_start: str
    interface: str
    priority: int

    def __init__(self, name: str):
        self.name = name

        if name not in self._get_config_all():
            raise sshtools.errors.NetworkNotFound(name)

        net_config: dict = self._get_config_all()[name]
        self.is_vpn = net_config.get("vpn", False)
        self.is_public = net_config.get("public", False)
        self.ip_start = net_config.get("ip_start", None)
        self.interface = net_config.get("interface", None)

        default_priority = 80
        if self.is_public:
            default_priority -= 30
        if self.is_vpn:
            default_priority -= 20

        self.priority = net_config.get("priority", default_priority)

    def __new__(cls, name: str, *_, **__):
        if name in cls.__instances:
            return cls.__instances[name]

        instance = super(Network, cls).__new__(cls)
        cls.__instances[name] = instance
        return instance

    @classmethod
    def _get_config_all(cls) -> dict:
        """
        Use getter to fix problems with python <3.9
        with combined property and classmethod decorators
        TODO: use @property when python >=3.9 can be ensured
        """
        if not cls.__config_all:
            cls.__config_all = {}
            for net_list_file in NETWORK_DIR.iterdir():
                net_list_config = json.load(net_list_file.open("r"))
                for net_config in net_list_config:
                    cls.__config_all[net_config["name"]] = net_config
        return cls.__config_all

    @property
    def is_connected(self) -> bool:
        """Is this device connected to this device?"""
        ip_list: sshtools.ip.IPAddressList = sshtools.ip.get_current_ips()
        if self.name == "public":
            return True

        if self.ip_start is not None:
            if any(self.has_ip_address(ip_address) for ip_address in ip_list):
                return True

        interfaces = psutil.net_if_addrs().keys()
        if self.interface is not None:
            if self.interface in interfaces:
                return True

        return False

    def get_interface(
        self, device: "sshtools.device.Device"
    ) -> typing.Optional[sshtools.interface.Interface]:
        """Returns an interface object for that the devices uses to connect to this network"""
        if self.interface is None:
            return None

        for interface in device.interfaces:
            if interface.name == self.interface:
                return interface
        return None

    def has_ip_address(self, ip_address: sshtools.ip.IPAddress) -> bool:
        """Is an ip address part of this network"""
        if isinstance(self.ip_start, str):
            return str(ip_address).startswith(self.ip_start)

        return False

    def construct_ip(self, device: "sshtools.device.Device") -> sshtools.ip.IPAddress:
        """
        Returns the IP for a device on this network based on the prefix of the network
        :param device: The device whose IP is requested, must have an ip_id
        """
        if device.ip_id is None:
            raise AttributeError(
                f"Device {device} must have a not-None ip_id attribute"
            )
        if self.ip_start is None:
            raise AttributeError(
                f"Network {self} must have a not-None ip_start attribute"
            )

        interface = self.get_interface(device)
        if interface is not None:
            interface_type = interface.type
        else:
            interface_type = None

        if (self.is_vpn or interface_type == "wifi") and device.ip_id < 155:
            ip_id = device.ip_id + 100
        else:
            ip_id = device.ip_id

        return sshtools.ip.IPAddress(self.ip_start + str(ip_id))

    @classmethod
    def get_networks(cls) -> list[Network]:
        """Get the IPs that the networks the current machine has access to"""
        networks: list[Network] = []

        network_names = cls._get_config_all().keys()
        for network_name in network_names:
            network = Network(network_name)
            if network is not None:
                networks.append(network)

        return networks

    @classmethod
    def get_connected_networks(cls) -> list[Network]:
        """Get the IPs that the networks the current machine has access to"""
        return list(filter(lambda n: n.is_connected, cls.get_networks()))

    def __repr__(self) -> str:
        return f"<sshtools.connection.Network '{self.name}'>"
