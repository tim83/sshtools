#! /usr/bin/python3
"""Module to obtain the IP adress of a device"""

from __future__ import annotations  # python -3.9 compatibility

import argparse
import concurrent.futures
import datetime as dt
import os

import timtools.log
from tabulate import tabulate

import sshtools.device
import sshtools.errors
import sshtools.sshin

logger = timtools.log.get_logger("ssh-tools.getip")


def get_ip_string(
    target: sshtools.device.Device,
    ssh_string: bool = False,
    strict_ip: bool = False,
    only_sshable: bool = False,
    only_moshable=False,
) -> str:
    """Return the full address of the user on the device"""

    if not target.is_present:
        return "x"

    ip_address = target.get_ip(
        strict_ip=strict_ip, only_sshable=only_sshable, only_moshable=only_moshable
    )
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
        "-m",
        "--mosh",
        help="Selecteer alleen maar IPs waar met MOSH naar geconnecteerd worden",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--ip",
        help="Gebruik alleen IP adressen en geen DNS of hostnamen",
        action="store_true",
    )
    parser.add_argument(
        "-w",
        "--write-log",
        help="Maak een logentry bij de target",
        action="store_true",
    )
    parser.add_argument(
        "-j",
        "--json",
        help="Geef de output als een json",
        action="store_true",
    )
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    targets: list[sshtools.device.Device]
    if len(args.target) == 0:
        targets = sshtools.device.DeviceConfig.get_devices(filter_main=True)
    else:
        targets = [sshtools.device.Device(name) for name in args.target]

    output: list[list[str]] = []

    def device_add_row(device: sshtools.device.Device):
        ip_string = get_ip_string(
            device,
            ssh_string=args.ssh_string,
            strict_ip=args.ip,
            only_sshable=args.ssh,
            only_moshable=args.mosh,
        )
        output.append([device.name, ip_string])

        if args.write_log is True:
            sshtools.sshin.Ssh(
                dev=device,
                exe=[
                    "echo",
                    f"{os.uname().nodename} accessed this device on {dt.datetime.now()}",
                    ">> /tmp/sshtools_access.txt",
                ],
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(device_add_row, targets)

    if args.write_log is True:
        return

    if args.json is True:

        def x_to_none(value: str):
            return None if value == "x" else value

        output_json: dict[str, str] = {
            device: x_to_none(ip_address) for device, ip_address in output
        }
        print(output_json)
        return

    if len(output) == 1:
        output_str = output[0][1]
        if output_str == "x":
            raise sshtools.errors.DeviceNotPresentError(targets[0].name)
        print(output_str)
    else:
        output_sorted = sorted(output, key=lambda r: r[0])
        print(tabulate(output_sorted, headers=["Device", "IP Address"]))


if __name__ == "__main__":
    run()
