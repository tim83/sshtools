#! /usr/bin/python3
"""Module to obtain the IP adress of a device"""

import argparse
import concurrent.futures
import datetime as dt
import os

import timtools.log
from tabulate import tabulate

import sshtools.errors
import sshtools.sshin
from sshtools.device import Device

logger = timtools.log.get_logger("ssh-tools.getip")


def get_ip_string(
    target: Device, ssh_string: bool = False, strict_ip: bool = False
) -> str:
    """Return the full address of the user on the device"""

    try:
        ip_address = target.get_ip(strict_ip=strict_ip)
        if ssh_string:
            user = target.user
            return f"{user}@{ip_address}"
        else:
            return str(ip_address)
    except (
        sshtools.errors.NotReachableError,
        sshtools.errors.DeviceNotPresentError,
    ):
        return "x"


def run():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target", help="Computer voor wie het ip adres moet worden bepaald", nargs="*"
    )
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    parser.add_argument(
        "-s",
        "--ssh-string",
        help="Geeft de volledige string voor SSH ([USER]@[IP])",
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
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    targets: list[Device]
    if len(args.target) == 0:
        targets = list(filter(lambda dev: dev.sync, Device.get_devices()))
    else:
        targets = [Device(name) for name in args.target]

    target: Device
    output: list[list[str]] = []

    def device_add_row(device: Device):
        ip_string = get_ip_string(device, ssh_string=args.ssh_string, strict_ip=args.ip)
        output.append([device.name, ip_string])

        if args.write_log and False:
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
