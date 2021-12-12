#!  /usr/bin/python3
"""Module to wake up devices using wake on lan"""

import argparse
import subprocess

from timtools import bash, log

from sshtools.devices import Device

logger = log.get_logger(__name__)


def wake(device: Device):
    """Wake up a device"""
    ip_addr: str = device.sort_ips(
        device.get_possible_ips(
            include_dns=False,
            include_wlan=False,
            include_hostname=False,
            include_eth=True,
        )
    )[0]
    mac_addr: str = device.emac

    try:
        cmd: list
        if ip_addr.startswith("192.168.2"):
            cmd = ["wol", mac_addr]
        elif ip_addr is not None:
            cmd = ["wol", "-p", str(device.ssh_port), "-i", ip_addr, mac_addr]
        else:
            raise ConnectionError()

        logger.debug(cmd)

        try:
            bash.run(cmd)
        except subprocess:
            bash.run(["sudo", "wakeonlan"] + cmd[1:])

    except ConnectionError:
        logger.critical("%s kan niet bereikt worden", device.hostname)


def run():
    """Main executable for wake-up"""
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Welke computer is de referentie", nargs="?")
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    args = parser.parse_args()
    log.set_verbose(args.verbose)

    devices = Device.get_device_names()
    logger.debug(devices)

    target = Device.get_device(args.target)
    wake(target)


if __name__ == "__main__":
    run()
