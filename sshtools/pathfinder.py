from __future__ import annotations  # python -3.9 compatibility

import typing

import timtools.log

import sshtools.connection
import sshtools.device
import sshtools.sshin
import sshtools.tools

logger = timtools.log.get_logger("sshtools.pathfinder")


class Path:
    device_route: list[sshtools.device.Device]

    def __init__(self, devices: list[sshtools.device.Device]):
        self.device_route = devices

    def is_reachable(self) -> bool:
        if not self.device_route[0].is_sshable():
            return False

        for index in range(1, len(self.device_route)):
            if not self.device_is_present_for_device(
                self.device_route[index - 1], self.device_route[index]
            ):
                return False

        return True

    @staticmethod
    def device_is_present_for_device(
        source: sshtools.device.Device, target: sshtools.device.Device
    ) -> bool:
        ssh_check = sshtools.sshin.Ssh(
            source,
            exe=f"python3 -m sshtools.getip {target.name} > /dev/null 2>/dev/null",
        )
        logger.critical(
            f"{target.name} can{'not' if not ssh_check.exe_was_successful else ''} be reached through "
            f"{source}"
        )
        return ssh_check.exe_was_successful

    def __repr__(self):
        dev_name_list = [dev.name for dev in self.device_route]
        return f"<sshtools.pathfinder.Path route={','.join(dev_name_list)}>"


class PathFinder:
    source: sshtools.device.Device
    target: sshtools.device.Device
    possible_paths: list[Path]
    path: typing.Optional[Path]

    def __init__(
        self, source: sshtools.device.Device, target: sshtools.device.Device = None
    ):
        if source is None:
            source = sshtools.device.Device.get_self()

        self.source = source
        self.target = target

    @property
    def possible_paths(self) -> list[Path]:
        possible_paths = []

        path = [self.target]
        if self.in_same_network(self.source, self.target):
            possible_paths.append(Path(path))

        relays = sshtools.tools.mt_filter(
            self.device_is_a_possible_relay,
            sshtools.device.Device.get_devices(),
        )

        for device in relays:
            possible_paths.append(Path([device] + path))

        return self.sort_paths(possible_paths)

    @staticmethod
    def sort_paths(paths: list[Path]) -> list[Path]:
        return sorted(paths, key=lambda p: len(p.device_route))

    def find_path(self):
        possible_path = self.possible_paths
        if self.source.is_self():
            return possible_path[0]

        for path in possible_path:
            if path.is_reachable():
                return path

    def device_is_a_possible_relay(self, device: sshtools.device.Device) -> bool:
        return (
            not device.is_self()
            and device.ssh is True
            and self.in_same_network(device, self.target)
        )

    @classmethod
    def in_same_network(
        cls, device1: sshtools.device.Device, device2: sshtools.device.Device
    ) -> bool:
        networks1 = cls.get_device_networks(device1)
        networks2 = cls.get_device_networks(device2)
        return any(
            network1 in networks2 for network1 in networks1 if not network1.is_public
        )

    @staticmethod
    def get_device_networks(
        device: sshtools.device.Device,
    ) -> list[sshtools.connection.Network]:
        ip_list = device.ip_address_list_all
        return [ip_address.network for ip_address in ip_list]
