#! /usr/bin/python3

from __future__ import annotations  # python -3.9 compatibility

import argparse
import datetime as dt
import os
import shutil
import socket
import subprocess
import tempfile
import uuid
from pathlib import Path

import timtools.bash
import timtools.locations
import timtools.log

import sshtools.device
import sshtools.errors
import sshtools.tools

logger = timtools.log.get_logger("sshtools.ssync")


class Sync:
    """Sync devices over the network using RSYNC"""

    dir: Path
    username: str
    hostname: str

    def __init__(
        self,
        master: sshtools.device.Device,
        slaves: list[sshtools.device.Device],
        dry_run: bool = False,
        force_limited: bool = False,
    ):
        self.hostname = socket.gethostname()
        self.username = os.environ["USER"]
        self.dir = Path.home()

        active_slaves: list[sshtools.device.Device] = sshtools.tools.mt_filter(
            lambda s: s.is_sshable is not False, slaves
        )

        tmp_dir: Path
        for slave in sorted(active_slaves, key=lambda d: d.priority):
            print()
            print(master.name + " -> " + slave.name)
            tmp_dir = Path(tempfile.mkdtemp())

            cmd = ["rsync"]
            cmd += [
                "--archive",
                "--verbose",
                "--human-readable",
                "-P",
                "--force",
                "--delete",
                "--compress",
                f'--partial-dir={self.get_cache_dir(slave) / "ssync"}',
            ]

            if not slave.is_self:
                port = slave.ssh_port
                cmd += ["-e", f"ssh -p {port}"]
            elif not master.is_self:
                port = master.ssh_port
                cmd += ["-e", f"ssh -p {port}"]

            if dry_run:
                cmd += ["--dry-run"]

            cmd += self.backup_parm(slave)
            cmd += self.inex_parm(master, slave, tmp_dir, force_limited=force_limited)
            cmd += self.get_source(master)
            cmd += self.get_target(slave)

            logger.debug(" ".join(cmd))
            try:
                timtools.bash.run(cmd)
            except subprocess.CalledProcessError as error:
                if error.returncode == 255:
                    if len(active_slaves) == 1:
                        raise sshtools.errors.NotReachableError(slave.name) from error
                    else:
                        logger.error(f"{slave} has disappeared.")
                raise error

            finally:
                shutil.rmtree(tmp_dir)

    def get_cache_dir(self, slave: sshtools.device.Device) -> Path:
        """
        Returns the cache directory to be used on the slave machine
        :param slave: The machine the cache directory will be on
        :return: The filepath to the cache directory on the slave machine
        """
        return timtools.locations.get_user_cache_dir(slave.user)

    def backup_parm(self, slave: sshtools.device.Device) -> list[str]:
        """
        Returns the rsync parameters pertaining to the backup of files
        :param slave: The device to sync to
        :return: A list of strings containing the rsync backup parameters
        """
        now = dt.datetime.now()
        random_str = str(uuid.uuid4()).split("-")[0]
        dirname = str(now.strftime("%H%M%S")) + "-" + random_str
        backup_dir = (
            self.get_cache_dir(slave)
            / "ssync_backup"
            / str(now.year)
            / str(now.month)
            / str(now.day)
            / dirname
        )
        return ["--backup", "--backup-dir={dir}".format(dir=backup_dir)]

    def inex_parm(
        self,
        master: sshtools.device.Device,
        slave: sshtools.device.Device,
        tmp_dir: Path,
        force_limited: bool = False,
    ) -> list[str]:
        """
        Returns the rsync parameters for excluding and including files
        :param master: The device to sync from
        :param slave: The device to sync to
        :param tmp_dir: The filepath to a temporary directory that is present for the whole sync process
        :param force_limited: Only sync a limited number of essential files
        :return: A list of strings that contains the rsync parameters for including and excluding files
        """
        in2file: Path = tmp_dir / "include_rest.txt"

        with open(in2file, "w") as fobj:
            rules: list[str] = [
                f"{d}/**\n" for d in os.listdir(self.dir) if not d.startswith(".")
            ]
            fobj.writelines(rules)

        def inexdir(path: Path) -> list[str]:
            inexlist: list[str] = []
            for inexfile in sorted(path.iterdir()):
                action: str
                if "include" in inexfile.stem:
                    action = "include"
                elif "exclude" in inexfile.stem:
                    action = "exclude"
                else:
                    raise ValueError(f"{inexfile} is not in the required format.")
                inexlist.append(f"--{action}-from={inexfile}")
            return inexlist

        if all(dev.sync is True for dev in (slave, master)) and not force_limited:
            return inexdir(sshtools.tools.CONFIG_DIR / "ssync")
        else:
            return inexdir(sshtools.tools.CONFIG_DIR / "ssync_limited")

    def get_source(self, master) -> list[str]:
        """
        Get the parameters for rsync identifying the source of the sync
        :param master: The device to sync from
        :return: A list of strings containing the sync source
        """
        source: list
        if master.is_self:
            source = [f"{self.dir}/"]
        else:
            source = [f"{master.user}@{master.ip_address}:{master.home}/"]
        return source

    def get_target(self, slave) -> list[str]:
        """
        Get the parameters for rsync identifying the target of the sync
        :param slave: The device to sync to
        :return: A list of strings containing the sync target
        """
        target: list[str]
        if slave.is_self:
            target = [f"{self.dir}"]
        else:
            target = [f"{slave.user}@{slave.ip_address}:{slave.home}/"]
        return target


def run():
    """Main executable for ssync"""
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("master", help="The device to sync from", nargs="?")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-f", "--from", help="Specify a manual source")
    parser.add_argument("-t", "--to", help="Specify a manual target")
    parser.add_argument(
        "-l",
        "--limited",
        help="Only sync a limited number of files",
        action="store_true",
    )
    parser.add_argument("-d", "--dry-run", action="store_true")
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    master: sshtools.device.Device
    slave: list[sshtools.device.Device]
    if getattr(args, "from") and args.to:
        # Define both SLAVE and MASTER
        master = sshtools.device.Device(getattr(args, "from").replace(" ", ""))
        slave = [sshtools.device.Device(args.to.replace(" ", ""))]
    elif getattr(args, "from") and not args.to:
        # Define only MASTER
        master = sshtools.device.Device(getattr(args, "from").replace(" ", ""))
        slave = [sshtools.device.Device.get_self()]
    elif not getattr(args, "from") and args.to:
        # Define only SLAVE
        master = sshtools.device.Device.get_self()
        slave = [sshtools.device.Device(args.to.replace(" ", ""))]
    else:
        if args.master:
            master = sshtools.device.Device(args.master)
        else:
            master = sshtools.device.Device.get_self()
        slave = sshtools.tools.mt_filter(
            lambda d: d != master and d.is_main_device and d.sync is not False,
            sshtools.device.Device.get_devices(),
        )

    if master in slave:
        raise argparse.ArgumentError(args.master, "Master kan geen slave zijn")

    super_devs: list[sshtools.device.Device] = sshtools.tools.mt_filter(
        lambda d: d.is_super, sshtools.device.Device.get_devices()
    )
    super_dev: sshtools.device.Device
    for super_dev in super_devs:
        if (
            super_dev in slave
            and super_dev.is_present
            and super_dev.sync is not False
            and (not args.dry_run)
        ):
            answer = input(
                f"Ben je zeker dat je naar {super_dev.name} wilt synchroniseren? (y/N) "
            )
            if answer.lower() not in ["y", "j"]:
                return

    Sync(master, slave, dry_run=args.dry_run, force_limited=args.limited)


if __name__ == "__main__":
    run()
