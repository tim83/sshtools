"""Module containing objects for storing the configuration of instances"""
from __future__ import annotations

import dataclasses
import typing

if typing.TYPE_CHECKING:
    import sshtools.connection


@dataclasses.dataclass
class ConnectionConfig:
    """Configuration of a Connection"""

    sync: typing.Union[bool, str]
    ssh: bool
    ssh_port: int
    mosh: bool
    user: str
    priority: int


@dataclasses.dataclass
class IPConnectionConfig(ConnectionConfig):
    """Configuration of an IPConnectionConfig"""

    network: "sshtools.connection.Network"
    check_online: bool
