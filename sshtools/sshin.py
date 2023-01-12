#! /usr/bin/python3
"""Module for connecting to a device using SSH or MOSH"""
from __future__ import annotations  # python -3.9 compatibility

import argparse
import os
import socket
import sys

import timtools.bash
import timtools.log

import sshtools.device
import sshtools.errors
import sshtools.ip
import sshtools.pathfinder

logger = timtools.log.get_logger("sshtools.sshin")


class Ssh:
    """Connect to a device using SSH"""

    exit_code: int = None
    exe_was_successful: bool = None

    def __init__(  # pylint: disable=too-many-arguments
        self,
        dev: sshtools.device.Device,
        exe: (str, list) = None,
        mosh: bool = None,
        copy_id: bool = False,
        user: str = None,
    ):
        logger.debug(
            "Device: %s ; Executable: %s ; Mosh: %s ; Copy ID: %s",
            dev.hostname,
            exe,
            mosh,
            copy_id,
        )

        self.device: sshtools.device.Device = dev
        if user is not None:
            self.device.config.user = user

        self.hostname: str = socket.gethostname()
        self.username: str = os.environ["USER"]

        if self.device.is_present and self.device.ssh:
            self.connect(exe=exe, copy_id=copy_id, mosh=mosh)
        else:
            self.relay_connect(exe=exe, mosh=mosh)

    def relay_connect(self, mosh: bool = None, exe: (str, list) = None):
        """Connect to the device using a relay"""
        # Alternative: use jump hosts
        # https://www.tecmint.com/access-linux-server-using-a-jump-host/
        logger.info(
            "%s could not be reached, trying to find an alternative path.",
            self.device,
        )
        pathfinder = sshtools.pathfinder.PathFinder(self.device)
        pathfinder.find_path()
        if pathfinder.path is None:
            raise sshtools.errors.NotReachableError(self.device.name)

        cmd = ["python3", f"-m sshtools.sshin {self.device}"]
        if mosh is True:
            cmd.append("--mosh")
        elif mosh is False:
            cmd.append("--ssh")

        if exe:
            if isinstance(exe, list):
                exe_string = '"' + '" "'.join(exe) + '"'
            else:
                exe_string = exe
            cmd.append(f"-c '{exe_string}'")
        Ssh(pathfinder.path.device_route[0], exe=cmd, mosh=mosh)

    def connect(
        self,
        exe: (str, list) = None,
        ssh_port: str = None,
        copy_id: bool = False,
        mosh: bool = None,
    ):
        """
        Actually connects to the device
        :param exe: The command to execute on the device (None opens an interactive terminal)
        :param ssh_port: The port to connect to for SSH
        :param copy_id: Copy the SSH keys from this machine to the target
        :param mosh: Use MOSH instead of SSH
        """
        ip_address = self.device.get_ip(only_sshable=True)
        user = self.device.user
        if not self.device.ssh:
            raise sshtools.errors.ConfigError(self.device.name)

        if isinstance(exe, list):
            exe = " ".join(exe)

        if ssh_port is None:
            ssh_port = str(self.device.ssh_port)

        if exe is None:
            self.print_header(ip_address)

        try:
            if copy_id:
                cmd_ci = ["ssh-copy-id", "-p", str(ssh_port), f"{user}@{ip_address}"]
                logger.debug(" ".join(cmd_ci))

                response_ci = timtools.bash.run(cmd_ci)
                logger.info("SSH-COPY-ID exited with code %s", response_ci.exit_code)
            if mosh is True or (mosh is None and self.device.mosh):
                cmd = ["mosh", f"{user}@{ip_address}"]
            else:
                cmd = ["ssh", "-t", "-p", str(ssh_port), f"{user}@{ip_address}"]

            if exe:
                cmd += [exe]

            logger.debug(" ".join(cmd))
            cmd_result = timtools.bash.run(
                cmd, passable_exit_codes=[255, "*"], capture_stderr=True
            )
            self.exit_code = cmd_result.exit_code
            if exe:
                self.exe_was_successful = self.exit_code == 0

            if __name__ == "__main__":
                sys.exit(self.exit_code)

        except ConnectionError:
            pass

        if exe is None:
            self.print_header(ip_address)

    def print_header(self, ip_address: sshtools.ip.IPAddress):
        """
        Prints a header to the terminal
        :param ip_address: The ip address to announce in the header
        """
        twidth = self.get_terminal_columns()

        print(f"Connecting to {ip_address} ...\n")
        print("-" * twidth + "\n")

    @staticmethod
    def get_terminal_columns() -> int:
        """Returns the width of the terminal"""
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80

    def print_footer(self):
        """Prints a footer to the terminal"""
        twidth = self.get_terminal_columns()
        print("\n" + "-" * twidth + "\n")


def run():
    """Main executable for sshin"""
    logger.debug(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="The name of the device to connect to.")
    parser.add_argument("-c", "--command", help="The command to execute on the TARGET.")
    parser.add_argument(
        "-u",
        "--user",
        help="Connect to this user on the target device.",
    )
    parser.add_argument(
        "-i",
        "--copy-id",
        help="Copy the SSH keys from this machine to the target.",
        action="store_true",
    )
    parser.add_argument(
        "-m", "--mosh", help="Use MOSH instead of SSH", action="store_true"
    )
    parser.add_argument("-s", "--ssh", help="Always use SSH.", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    logger.debug(args)

    timtools.log.set_verbose(args.verbose)

    target = sshtools.device.Device(args.target)

    if args.mosh:
        use_mosh = True
    elif args.ssh:
        use_mosh = False
    else:
        use_mosh = None
    Ssh(target, exe=args.command, mosh=use_mosh, copy_id=args.copy_id, user=args.user)


if __name__ == "__main__":
    run()
