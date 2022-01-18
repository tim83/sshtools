from __future__ import annotations  # python -3.9 compatibility

import dataclasses
import json
import socket
from pathlib import Path
from typing import Union

import psutil
from cachetools.func import ttl_cache
from timtools.log import get_logger

from sshtools import errors, ip, tools
from sshtools.errors import NetworkError

logger = get_logger("sshtools.connection")

NETWORK_DIR: Path = tools.CONFIG_DIR / "networks"


@ttl_cache(ttl=3)
def get_current_ips() -> ip.IPAddressList:
    """Get the IPs that the current device has assigned"""
    interface_data = psutil.net_if_addrs()
    interface_names = sorted(interface_data.keys())
    addresses = ip.IPAddressList()
    for interface_name in interface_names:
        try:
            ip_addr_list = ip.IPAddressList(
                [
                    ip.IPAddress(address.address)
                    for address in interface_data[interface_name]
                    if address.family == socket.AF_INET
                ]
            )
            addresses.add_list(ip_addr_list)
        except StopIteration:
            pass
    if addresses.length() == 0:
        raise NetworkError()

    logger.debug(
        f"This machine has {addresses.length()} ip addresses: {addresses.to_list()}"
    )

    return addresses


class Network:
    __instances: dict[str, Network] = {}
    __config_all: dict[str, dict] = None
    name: str
    is_vpn: bool
    is_public: bool
    ip_start: str
    interface: str

    def __init__(self, name: str):
        self.name = name

        if name not in self._get_config_all().keys():
            raise errors.NetworkNotFound(name)

        net_config: dict = self._get_config_all()[name]
        self.is_vpn = net_config.get("vpn", False)
        self.is_public = net_config.get("public", False)
        self.ip_start = net_config.get("ip_start", None)
        self.interface = net_config.get("interface", None)

    def __new__(cls, name: str, *args, **kwargs):
        if name in cls.__instances.keys():
            return cls.__instances[name]

        instance = super(Network, cls).__new__(cls)
        cls.__instances[name] = instance
        return instance

    @classmethod
    def _get_config_all(cls) -> dict:
        """
        Use getter to fix problems with python <3.9 with combined property and classmethod decorators
        TODO: use @property when python >=3.9 can be ensured
        """
        if cls.__config_all is None:
            cls.__config_all = {}
            for net_list_file in NETWORK_DIR.iterdir():
                net_list_config = json.load(net_list_file.open("r"))
                for net_config in net_list_config:
                    cls.__config_all[net_config["name"]] = net_config
        return cls.__config_all

    @property
    def is_connected(self) -> bool:
        ip_list: ip.IPAddressList = get_current_ips()
        if self.name == "public":
            return True

        if self.ip_start is not None:
            if any(str(ip_address).startswith(self.ip_start) for ip_address in ip_list):
                return True

        interfaces = psutil.net_if_addrs().keys()
        if self.interface is not None:
            if self.interface in interfaces:
                return True

        return False

    @classmethod
    def get_networks(cls) -> list[Network]:
        """Get the IPs that the networks the current machine has access to"""
        connected_networks: list[Network] = []

        network_names = cls._get_config_all().keys()
        for network_name in network_names:
            network = Network(network_name)
            if network is not None and network.is_connected:
                connected_networks.append(network)

        return connected_networks

    def __repr__(self) -> str:
        return f"<sshtools.connection.Network '{self.name}'>"


@dataclasses.dataclass
class ConnectionConfig:
    sync: Union[bool, str]
    ssh: bool
    ssh_port: int
    mosh: bool
    user: str
    priority: int


@dataclasses.dataclass
class IPConnectionConfig(ConnectionConfig):
    network: Network
    check_online: bool
