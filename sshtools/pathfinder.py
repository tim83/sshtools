import typing

import timtools.log

import sshtools.connection
import sshtools.device
import sshtools.sshin
import sshtools.tools

logger = timtools.log.get_logger("sshtools.pathfinder")


class PathFinder:
    source: sshtools.device.Device
    target: sshtools.device.Device
    path: typing.Optional[list[sshtools.device.Device]]

    def __init__(
        self, target: sshtools.device.Device, source: sshtools.device.Device = None
    ):
        if source is None:
            source = sshtools.device.Device.get_self()

        self.source = source
        self.target = target

    def find_path(self):
        self.path = [self.target]
        if self.target.is_present():
            return

        possible_devices = sshtools.tools.mt_filter(
            self.device_is_a_possible_relay,
            sshtools.device.Device.get_devices(),
        )
        for device in possible_devices:
            self.path.insert(0, device)
            return

        self.path = None

    def device_is_a_possible_relay(self, device: sshtools.device.Device) -> bool:
        return (
            not device.is_self()
            and device.ssh is True
            and self.in_same_network(device, self.target)
            and device.is_present()
            and self.device_is_present_for_device(device, self.target)
        )

    @staticmethod
    def device_is_present_for_device(
        source: sshtools.device.Device, target: sshtools.device.Device
    ) -> bool:
        ssh_check = sshtools.sshin.Ssh(
            source,
            exe=f"python3 -m sshtools.getip {target.name} > /dev/null 2>/dev/null",
        )
        logger.critical(
            f"{target.name} can{'not' if not ssh_check.exe_was_succesfull else ''} be reached through {source}"
        )
        return ssh_check.exe_was_succesfull

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
