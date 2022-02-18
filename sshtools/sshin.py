#! /usr/bin/python3
"""Module to ssh into a device"""

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
    """Class to ssh into a device"""

    exit_code: int = None
    exe_was_succesfull: bool = None

    def __init__(
        self,
        dev: sshtools.device.Device,
        exe: (str, list) = None,
        mosh: bool = False,
        copy_id: bool = False,
        connect: bool = True,
    ):
        if connect:
            logger.debug(
                "Device: %s ; Executable: %s ; Mosh: %s ; Copy ID: %s",
                dev.hostname,
                exe,
                mosh,
                copy_id,
            )
        else:
            logger.debug("Device: %s", dev.hostname)

        self.device: sshtools.device.Device = dev
        self.hostname: str = socket.gethostname()
        self.username: str = os.environ["USER"]

        if connect:
            if self.device.is_present():
                self.connect(exe=exe, copy_id=copy_id, mosh=mosh)
            else:
                logger.warning(
                    f"{self.device.name} could not be reached, trying to find an alternative path."
                )
                pf = sshtools.pathfinder.PathFinder(self.device)
                pf.find_path()
                if pf.path is None:
                    raise sshtools.errors.NotReachableError(self.device.name)

                cmd = f"python3 -m sshtools.sshin {self.device}"
                if mosh:
                    cmd += "--mosh"
                if exe:
                    if isinstance(exe, list):
                        exe_string = '"' + '" "'.join(exe) + '"'
                    else:
                        exe_string = exe
                    cmd += f"-c {exe_string}"
                Ssh(pf.path[0], exe=cmd)

    def connect(
        self,
        exe: (str, list) = None,
        ssh_port: str = None,
        copy_id: bool = False,
        mosh: bool = False,
    ):
        ip_address = self.device.ip_address
        user = self.device.user
        if not self.device.ssh:
            raise sshtools.errors.ConfigError(self.device.name)

        if isinstance(exe, list):
            exe = " ".join(exe)

        if ssh_port is None:
            ssh_port = str(self.device.ssh_port)
        else:
            ssh_port = ssh_port

        if exe is None:
            self.print_header(ip_address)

        try:
            if copy_id:
                cmd_ci = ["ssh-copy-id", "-p", str(ssh_port), f"{user}@{ip_address}"]
                logger.debug(" ".join(cmd_ci))

                response_ci = timtools.bash.run(cmd_ci)
                logger.info("SSH-COPY-ID exited with code %s", response_ci.exit_code)
            if mosh and self.device.is_local():
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
                self.exe_was_succesfull = self.exit_code == 0

            if __name__ == "__main__":
                sys.exit(self.exit_code)

        except ConnectionError:
            pass

        if exe is None:
            self.print_header(ip_address)

    def print_header(self, ip_addr: sshtools.ip.IPAddress):
        """Prints a header to the terminal"""
        twidth = self.get_terminal_columns()

        print(f"Connecting to {ip_addr} ...\n")
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
    parser.add_argument("target", help="Welke computer is de referentie")
    parser.add_argument("-c", "--command", help="Uit te voeren commando")
    parser.add_argument(
        "-u",
        "--user",
        help="Login als deze gebruiker, in plaats van de standaard gebruiker",
    )
    parser.add_argument(
        "-i",
        "--copy-id",
        help="Voert ssh-copy-id uit voor de verbinden",
        action="store_true",
    )
    parser.add_argument(
        "-m", "--mosh", help="Gebruik MOSH in plaats van SSH", action="store_true"
    )
    parser.add_argument(
        "-s", "--ssh", help="Gebruik MOSH in plaats van SSH", action="store_true"
    )
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    args = parser.parse_args()
    logger.debug(args)

    timtools.log.set_verbose(args.verbose)

    target = sshtools.device.Device(args.target)

    if args.mosh:
        use_mosh = True
    elif args.ssh:
        use_mosh = False
    else:
        use_mosh = target.config.mosh
    Ssh(target, exe=args.command, mosh=use_mosh, copy_id=args.copy_id)


if __name__ == "__main__":
    run()
