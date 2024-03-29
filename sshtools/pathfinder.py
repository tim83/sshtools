"""Module for finding a relay path to a device"""
from __future__ import annotations  # python -3.9 compatibility

import typing

import timtools.log

import sshtools.connection
import sshtools.device
import sshtools.sshin
import sshtools.tools

logger = timtools.log.get_logger("sshtools.pathfinder")


class Path:
    """A path to a device"""

    device_route: list[sshtools.device.Device]

    def __init__(self, devices: list[sshtools.device.Device]):
        self.device_route = devices

    def is_reachable(self) -> bool:
        """Are all devices in the path SSHable?"""
        if not self.device_route[0].is_sshable:
            return False

        for index in range(1, len(self.device_route)):
            if not self.device_is_present_for_device(
                self.device_route[index - 1], self.device_route[index]
            ):
                return False

        return True

    @property
    def length(self) -> int:
        """How many devices are needed to complete the path?"""
        return len(self.device_route)

    @staticmethod
    def device_is_present_for_device(
        source: sshtools.device.Device, target: sshtools.device.Device
    ) -> bool:
        """Can devices reach each other?"""
        ssh_check = sshtools.sshin.Ssh(
            source,
            exe=f"python3 -m sshtools.getip {target} > /dev/null 2>/dev/null",
            mosh=False,
        )
        logger.info(
            "%s can%s be reached through %s",
            target,
            "not" if not ssh_check.exe_was_successful else "",
            source,
        )
        return ssh_check.exe_was_successful

    def __repr__(self):
        dev_name_list = [dev.name for dev in self.device_route]
        return f"<sshtools.pathfinder.Path route={'->'.join(dev_name_list)}>"


class PathFinder:
    """Class for selecting a path between devices"""

    source: sshtools.device.Device
    target: sshtools.device.Device
    path: typing.Optional[Path] = None

    def __init__(
        self, target: sshtools.device.Device, source: sshtools.device.Device = None
    ):
        if source is None:
            source = sshtools.device.Device.get_self()

        self.source = source
        self.target = target

    @property
    def possible_paths(self) -> list[Path]:
        """Determine all possible paths between devices"""
        possible_paths = []

        path = [self.target]
        if self.target.is_self:
            return [Path(path)]

        if self.in_same_network(self.source, self.target):
            possible_paths.append(Path(path))

        relays = sshtools.tools.mt_filter(
            self.device_is_a_possible_relay,
            sshtools.device.DeviceConfig.get_devices(),
        )

        for device in relays:
            possible_paths.append(Path([device] + path))

        return self.sort_paths(possible_paths)

    @staticmethod
    def sort_paths(paths: list[Path]) -> list[Path]:
        """Sort the paths by their length (sortest path first)"""
        return sorted(paths, key=lambda p: p.length)

    def find_path(self) -> typing.Optional[Path]:
        """
        Returns the shorted alive path
        :return: Path or None
        """
        alive_paths = sshtools.tools.mt_filter(
            lambda p: p.is_reachable(), self.possible_paths
        )
        if len(alive_paths) > 0:
            self.path = self.sort_paths(alive_paths)[0]
            return self.path

        return None

    def device_is_a_possible_relay(self, device: sshtools.device.Device) -> bool:
        """Is a device a possible relay?"""
        return (
            not device.is_self
            and device != self.target
            and device.ssh is True
            and self.in_same_network(device, self.target)
        )

    @classmethod
    def in_same_network(
        cls, device1: sshtools.device.Device, device2: sshtools.device.Device
    ) -> bool:
        """Are devices in the same network?"""
        networks1 = cls.get_device_networks(device1)
        networks2 = cls.get_device_networks(device2)
        return any(
            network1 in networks2 for network1 in networks1 if not network1.is_public
        )

    @staticmethod
    def get_device_networks(
        device: sshtools.device.Device,
    ) -> list[sshtools.connection.Network]:
        """Get the list of networks a device can connect to"""
        ip_list = device.ip_address_list_all
        return [ip_address.network for ip_address in ip_list]
