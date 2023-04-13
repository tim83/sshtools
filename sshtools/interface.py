"""Module for managing network interfaces"""
from __future__ import annotations  # python -3.9 compatibility

from typing import TYPE_CHECKING

import timtools.bash

import sshtools.tools

if TYPE_CHECKING:
    # Circular import
    import sshtools.device


class Interface:  # pylint: disable=too-few-public-methods
    """Class representing a network interface"""

    device: "sshtools.device.Device"
    name: str
    type: str
    mac: str

    def __init__(self, device: "sshtools.device.Device", name: str, mac: str = None):
        self.device = device
        self.name = name
        self.type = self._determine_interface_type(name)

        self.mac = mac

    @staticmethod
    def _determine_interface_type(name) -> str:
        if name.startswith("eth") or name.startswith("enp"):
            return "wired"
        if name.startswith("wlan") or name.startswith("wlp"):
            return "wifi"

        return "unknown"

    def wake(self):
        """Send a magic packet to this interface using wake on lan"""
        cmd: list[str]
        possible_wol_exec: list[str] = ["wol", "wakeonlan"]
        for wol_exec in possible_wol_exec:
            if sshtools.tools.execute_is_present(wol_exec):
                cmd = [wol_exec]
                break
        else:
            possible_wol_exec_string: str = "'" + "', '".join(possible_wol_exec) + "'"
            raise FileNotFoundError(
                f"No executable for wake on lan could be found (tried {possible_wol_exec_string})"
            )

        cmd += [self.mac]
        timtools.bash.run(cmd)

    def __repr__(self):
        return f"<sshtools.interface.Interface {self.name} ({self.type})"
