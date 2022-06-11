#! /usr/bin/python3
"""Module for syncing between devices"""
from __future__ import annotations  # python -3.9 compatibility

import argparse
import datetime as dt
import os
import shutil
import socket
import subprocess
import typing
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

    master: sshtools.device.Device
    slaves: list[sshtools.device.Device]
    dry_run: bool
    force_limited: bool

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

        self.master = master
        self.slaves = slaves
        self.dry_run = dry_run
        self.force_limited = force_limited

        active_slaves: list[sshtools.device.Device] = sshtools.tools.mt_filter(
            lambda s: s.is_sshable is True, self.slaves
        )

        tmp_dir: Path
        for slave in sorted(active_slaves, key=lambda d: d.priority):
            print(f"\n{self.master} -> {slave}")

            tmp_dir = sshtools.tools.get_tmp_dir()
            cmd = self.get_cmd(slave, tmp_dir)

            logger.debug(" ".join(cmd))
            try:
                timtools.bash.run(cmd)
            except subprocess.CalledProcessError as error:
                if error.returncode == 255:
                    if len(active_slaves) == 1:
                        raise sshtools.errors.NotReachableError(slave.name) from error
                    logger.error("%s has disappeared.", slave)
                raise error

            finally:
                shutil.rmtree(tmp_dir)

    def get_cmd(self, slave: sshtools.device.Device, tmp_dir: Path) -> list[str]:
        """
        Returns the command for syncing to a certain device
        :param slave: The device to sync to
        :param tmp_dir: A temporary directory that exists
        :return: A list of strings
        """
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
        elif not self.master.is_self:
            port = self.master.ssh_port
            cmd += ["-e", f"ssh -p {port}"]

        if self.dry_run:
            cmd += ["--dry-run"]

        cmd += self.backup_parm(slave)
        cmd += self.inex_parm(
            self.master, slave, tmp_dir, force_limited=self.force_limited
        )
        cmd += self.get_source(self.master)
        cmd += self.get_target(slave)
        return cmd

    @staticmethod
    def get_cache_dir(slave: sshtools.device.Device) -> Path:
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
        random_str = str(uuid.uuid4()).split("-", maxsplit=1)[0]
        dirname = str(now.strftime("%H%M%S")) + "-" + random_str
        backup_dir = (
            self.get_cache_dir(slave)
            / "ssync_backup"
            / str(now.year)
            / str(now.month)
            / str(now.day)
            / dirname
        )
        return ["--backup", f"--backup-dir={backup_dir}"]

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
        :param tmp_dir: The path to a temporary directory
        :param force_limited: Only sync a limited number of essential files
        :return: A list of strings that contains the rsync parameters for selecting files
        """
        in2file: Path = tmp_dir / "include_rest.txt"

        with open(in2file, "w", encoding="utf-8") as fobj:
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


def get_relevant_devices(
    master_arg: typing.Optional[str],
    from_arg: typing.Optional[str],
    to_arg: typing.Optional[str],
) -> (sshtools.device.Device, list[sshtools.device.Device]):
    """
    Determine the devices that are involved in the transaction
    :param master_arg: The device that is to be used as the master (or none)
    :param from_arg: The device that is selected in the from field (or none)
    :param to_arg: The device that is selected in the to field (or none)
    :return: The master device and the list of slave devices
    """
    if from_arg and to_arg:
        # Define both SLAVE and MASTER
        master = sshtools.device.Device(from_arg)
        slaves = [sshtools.device.Device(to_arg)]
    elif from_arg and not to_arg:
        # Define only MASTER
        master = sshtools.device.Device(from_arg.replace(" ", ""))
        slaves = [sshtools.device.Device.get_self()]
    elif not from_arg and to_arg:
        # Define only SLAVE
        master = sshtools.device.Device.get_self()
        slaves = [sshtools.device.Device(to_arg.replace(" ", ""))]
    else:
        if master_arg:
            master = sshtools.device.Device(master_arg)
        else:
            master = sshtools.device.Device.get_self()
        slaves = sshtools.tools.mt_filter(
            lambda d: d != master and d.is_main_device and d.sync is not False,
            sshtools.device.DeviceConfig.get_devices(),
        )

    if master in slaves:
        raise argparse.ArgumentError(master_arg, "Master kan geen slaves zijn")

    return master, slaves


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
    slaves: list[sshtools.device.Device]
    master, slaves = get_relevant_devices(args.master, getattr(args, "from"), args.to)
    super_devs: list[sshtools.device.Device] = sshtools.device.DeviceConfig.get_devices(
        filter_super=True
    )
    super_dev: sshtools.device.Device
    for super_dev in super_devs:
        if (
            super_dev in slaves
            and super_dev.is_present
            and super_dev.sync is not False
            and (not args.dry_run)
        ):
            answer = input(
                f"Ben je zeker dat je naar {super_dev} wilt synchroniseren? (y/N) "
            )
            if answer.lower() not in ["y", "j"]:
                return
    Sync(master, slaves, dry_run=args.dry_run, force_limited=args.limited)


if __name__ == "__main__":
    run()
