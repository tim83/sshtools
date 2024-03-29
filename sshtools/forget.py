"""Module to remove all entries of a machine in .ssh/known_hosts"""

from __future__ import annotations  # python -3.9 compatibility

import argparse

import timtools.bash
import timtools.locations
import timtools.log

import sshtools.device

logger = timtools.log.get_logger("ssh-tools.forget")


def forget_device(target: sshtools.device.Device):
    """
    Remove all entries for a device in .ssh/known_hosts
    :param target: The device whose entries need to be removed
    """
    ips = target.get_possible_ips(
        include_dns=True, include_ips=True, include_hostname=True
    )
    ips.add_list(target.ip_address_list_all)
    for ip_address in ips:
        timtools.bash.run(
            ["ssh-keygen", "-R", str(ip_address)],
            capture_stderr=True,
            capture_stdout=True,
        )
        host_id: str = timtools.bash.get_output(
            ["ssh-keyscan", str(ip_address)], passable_exit_codes=["*"]
        )
        known_host_file = timtools.locations.get_user_home() / ".ssh/known_hosts"
        with open(known_host_file, "a", encoding="utf-8") as kh_file:
            kh_file.write(host_id)


def run():
    """Run ssh-forget"""
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="De machine om te vergeten", nargs="*")
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    for target in args.target:
        forget_device(sshtools.device.DeviceConfig.get_device(target))


if __name__ == "__main__":
    run()
