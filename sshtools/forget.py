#! /usr/bin/python3
"""Module to remove all entries of a machine in .ssh/known_hosts"""

import argparse

import timtools.bash
import timtools.log

from sshtools.device import Device

logger = timtools.log.get_logger("ssh-tools.remove-keys")


def forget_device(target: Device):
    ips = target.get_possible_ips(
        include_dns=True, include_ips=True, include_hostname=True
    ).add_list(target.ip_address_list_all)
    for ip in ips:
        timtools.bash.run(
            ["ssh-keygen", "-R", ip], capture_stderr=True, capture_stdout=True
        )


def run():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="De machine om te vergeten", nargs="*")
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    for target in args.target:
        forget_device(Device.get_device(target))


if __name__ == "__main__":
    run()
