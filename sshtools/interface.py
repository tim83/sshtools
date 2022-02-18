from __future__ import annotations  # python -3.9 compatibility

import subprocess
from typing import TYPE_CHECKING

import timtools.bash

if TYPE_CHECKING:
    # Circular import
    import sshtools.device


class Interface:
    device: "sshtools.device.Device"
    name: str
    type: str
    mac: str

    def __init__(self, device: "sshtools.device.Device", name: str, mac: str = None):
        self.device = device
        self.name = name
        if name.startswith("eth"):
            self.type = "wired"
        elif name.startswith("wlan"):
            self.type = "wifi"
        else:
            self.type = "unknown"

        self.mac = mac

    def wake(self):
        try:
            timtools.bash.run(["wol", self.mac])
        except subprocess.CalledProcessError:
            timtools.bash.run(["sudo", "wakeonlan", self.mac])
