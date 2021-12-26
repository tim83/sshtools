#! /usr/bin/python3
"""Module to obtain the IP adress of a device"""

import argparse
import datetime as dt
import os

import timtools.log

import sshtools.errors
import sshtools.sshin
import sshtools.ssync
from sshtools.devices import Device

logger = timtools.log.get_logger("ssh-tools.getip")


def get_string(target: Device) -> str:
    """Return the full address of the user on the device"""
    ip_addr = target.ip_address
    return f"{target.user}@{ip_addr}"


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

    target_names: list[str]
    limit_sync: bool = False
    if len(args.target) == 0:
        target_names = Device.get_device_names()
        limit_sync = True
        # target_names = ["laptop", "thinkcentre", "fujitsu", "probook", "serverpi", "camerapi"]
    else:
        target_names = args.target

    targets_all: list[Device] = [
        Device.get_device(target_name) for target_name in target_names
    ]

    # Lookup IPs in multithreading
    targets = sshtools.ssync.get_active_devices(targets_all, limit_sync=limit_sync)

    target: Device
    for target in targets:
        ip_string: str
        try:
            if args.ssh_string:
                ip_string = get_string(target)
            else:
                ip_string = target.ip_address
        except (
            sshtools.errors.NotReachableError,
            sshtools.errors.DeviceNotPresentError,
        ):
            ip_string = "none"

        if args.write_log:
            sshtools.sshin.Ssh(
                dev=target,
                exe=[
                    "echo",
                    f"{os.uname().nodename} accessed this device on {dt.datetime.now()}",
                    ">> /tmp/sshtools_access.txt",
                ],
            )
        else:
            if len(target_names) == 1:
                print(ip_string)
            else:
                print(f"{target.name}:\t{ip_string}")


if __name__ == "__main__":
    run()
