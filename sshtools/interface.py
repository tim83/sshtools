"""Module for managing network interfaces"""
from __future__ import annotations  # python -3.9 compatibility

from typing import TYPE_CHECKING

import timtools.bash

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
        wol_present_check = timtools.bash.run(
            ["which", "wol"], passable_exit_codes=[0, 1]
        )
        if wol_present_check.exit_code == 0:
            timtools.bash.run(["wol", self.mac])
        else:
            timtools.bash.run(["sudo", "wakeonlan", self.mac])
