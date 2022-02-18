#! /usr/bin/python3
"""Mounts a device using sftp"""

from __future__ import annotations  # python -3.9 compatibility

import argparse
import os
import socket
import subprocess
from pathlib import Path

import timtools.log

import sshtools.device
import sshtools.errors

logger = timtools.log.get_logger(__name__)


class Mount:
    """Mounts a source directory of a device on mountpoint"""

    def __init__(
        self,
        device: sshtools.device.Device,
        src: str,
        mountpoint: Path,
        open_mountpoint: bool = False,
        be_root: bool = False,
    ):
        logger.debug("Device: %s ; Source %s ; Mountpoint %s", device, src, mountpoint)

        self.hostname = socket.gethostname()
        self.username = os.environ["USER"]
        if not device.ssh:
            raise sshtools.errors.ConfigError(device.name)
        ip_addr = device.ip_address

        cmd = [
            "mount",
            "-t",
            "fuse.sshfs",
            "-o",
            "user,_netdev,reconnect,uid=1000,gid=1000,allow_other",
            f"{device.user}@{ip_addr}:{src}",
            f"{mountpoint}",
        ]
        if be_root:
            cmd.insert(0, "sudo")

        logger.debug(" ".join(cmd))
        response = subprocess.call(cmd)
        if response != 0:
            print(f"Responsecode from SSH: {response}")
        else:
            if open_mountpoint:
                subprocess.call(["xdg-open", mountpoint])

    @classmethod
    def print_header(cls, ip_addr: str):
        """Prints a header to the terminal"""
        os.system("clear")
        try:
            twidth = os.get_terminal_size().columns

            print(f"Connecting to {ip_addr} ...\n")
            print("-" * twidth + "\n")
        except OSError:
            pass

    @classmethod
    def print_footer(cls):
        """Prints a footer to the terminal"""
        twidth = os.get_terminal_size().columns
        print("\n" + "-" * twidth + "\n")


def run():
    """Main executable class for smount"""
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Welke computer is de referentie")
    parser.add_argument(
        "source",
        help="Locatie op taget die gemount moet worden",
        nargs="?",
        default="/home/tim",
    )
    parser.add_argument("mountpoint", help="Mountpoint")
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    parser.add_argument(
        "-r", "--root", help="Koppel de locatie aan als ROOT", action="store_true"
    )
    parser.add_argument("-o", "--open", help="Open het mountpoint", action="store_true")
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    target = sshtools.device.Device(args.target)
    source = args.source
    mountpoint = Path(args.mountpoint)

    Mount(target, source, mountpoint, open_mountpoint=args.open, be_root=args.root)


if __name__ == "__main__":
    run()
