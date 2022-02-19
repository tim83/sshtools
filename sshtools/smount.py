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

logger = timtools.log.get_logger("sshtools.smount")


class Mount:
    """Mounts a source directory of a device on mount point"""

    def __init__(
        self,
        device: sshtools.device.Device,
        src: str,
        mount_point: Path,
        open_mount_point: bool = False,
        be_root: bool = False,
    ):
        logger.debug(
            "Device: %s ; Source %s ; Mount point %s", device, src, mount_point
        )

        self.hostname = socket.gethostname()
        self.username = os.environ["USER"]
        if not device.ssh:
            raise sshtools.errors.ConfigError(device.name)
        ip_address = device.ip_address

        cmd = [
            "mount",
            "-t",
            "fuse.sshfs",
            "-o",
            "user,_netdev,reconnect,uid=1000,gid=1000,allow_other",
            f"{device.user}@{ip_address}:{src}",
            f"{mount_point}",
        ]
        if be_root:
            cmd.insert(0, "sudo")

        logger.debug(" ".join(cmd))
        response = subprocess.call(cmd)
        if response != 0:
            print(f"Response code from SSH: {response}")
        else:
            if open_mount_point:
                subprocess.call(["xdg-open", mount_point])

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
    parser.add_argument("target", help="Which device will be mounted.")
    parser.add_argument(
        "source",
        help="The location on the TARGET that will be mounted.",
        nargs="?",
        default="/home/tim",
    )
    parser.add_argument(
        "mountpoint",
        help="The location on this machine where the source will be mounted.",
    )
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    parser.add_argument("-r", "--root", help="Mount as root", action="store_true")
    parser.add_argument(
        "-o", "--open", help="Open the mount point after mounting", action="store_true"
    )
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    target = sshtools.device.Device(args.target)
    source = args.source
    mount_point = Path(args.mountpoint)

    Mount(target, source, mount_point, open_mount_point=args.open, be_root=args.root)


if __name__ == "__main__":
    run()
