#! /usr/bin/python3
"""Module to obtain the IP address of a device"""

from __future__ import annotations  # python -3.9 compatibility

import argparse

import timtools.log

import sshtools.device
import sshtools.errors
import sshtools.sshin
import sshtools.tools

logger = timtools.log.get_logger("ssh-tools.getip")


def get_ip_string(
    target: sshtools.device.Device,
    ssh_string: bool = False,
    strict_ip: bool = False,
    only_sshable: bool = False,
) -> str:
    """Return the full address of the user on the device"""

    if not target.is_present:
        return "x"

    ip_address = target.get_ip(strict_ip=strict_ip, only_sshable=only_sshable)
    if ssh_string:
        user = target.user
        return f"{user}@{ip_address}"

    return str(ip_address)


def run():
    """Run getip"""
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target", help="Computer voor wie het ip adres moet worden bepaald", nargs="*"
    )
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    parser.add_argument(
        "--ssh-string",
        help="Geeft de volledige string voor SSH ([USER]@[IP])",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--ssh",
        help="Selecteer alleen maar IPs waar met SSH naar geconnecteerd worden",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--ip",
        help="Gebruik alleen IP adressen en geen DNS of hostnamen",
        action="store_true",
    )
    parser.add_argument(
        "-j",
        "--json",
        help="Print de output in json",
        action="store_true",
    )
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    targets: list[sshtools.device.Device]
    if len(args.target) == 0:
        targets = sshtools.device.DeviceConfig.get_devices(filter_main=True)
    else:
        targets = [sshtools.device.Device(name) for name in args.target]

    def device_add_row(rows: list[list[str]], device: sshtools.device.Device):
        ip_string = get_ip_string(
            device,
            ssh_string=args.ssh_string,
            strict_ip=args.ip,
            only_sshable=args.ssh,
        )
        rows.append([device.name, ip_string])

    if args.json is True:
        output = []
        sshtools.tools.mt_map(lambda r: device_add_row(output, r), targets)
        print(
            {
                device: (ip_address if ip_address != "x" else None)
                for device, ip_address in output
            }
        )
        return

    if len(targets) == 1:
        output = []
        device_add_row(output, targets[0])
        output_str = output[0][1]
        if output_str == "x":
            raise sshtools.errors.DeviceNotPresentError(targets[0].name)
        print(output_str)
    else:
        print(
            sshtools.tools.create_table(
                device_add_row,
                targets,
                sorting_key=lambda r: r[0],
                headers=["Device", "IP Address"],
            )
        )


if __name__ == "__main__":
    run()
