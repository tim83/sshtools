import dataclasses
import typing

import sshtools.connection


@dataclasses.dataclass
class ConnectionConfig:
    sync: typing.Union[bool, str]
    ssh: bool
    ssh_port: int
    mosh: bool
    user: str
    priority: int


@dataclasses.dataclass
class IPConnectionConfig(ConnectionConfig):
    network: "sshtools.connection.Network"
    check_online: bool
