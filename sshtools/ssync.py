#! /usr/bin/python3
"""Syncs devices over LAN"""

from __future__ import annotations  # python -3.9 compatibility

import argparse
import datetime as dt
import os
import shutil
import subprocess
import tempfile
import threading
import uuid
from os.path import abspath, dirname, expanduser, join
from typing import Optional

import timtools.bash
import timtools.log

from sshtools.devices import Device
from sshtools.errors import NotReachableError

PROJECT_DIR: str = dirname(__file__)
logger = timtools.log.get_logger(__name__)


class Sync:
    """Sync devices"""

    dir: str
    username: str
    hostname: str

    def __init__(self, master: Device, slaves: list[Device], dry_run: bool = False):
        self.hostname = os.uname().nodename
        self.username = os.environ["USER"]
        self.dir = expanduser("~")

        active_slaves = get_active_devices(slaves)

        tmp_dir: str
        for slave in active_slaves:
            if not slave.sync or not slave.is_present():
                continue
            print()
            print(master.name + " -> " + slave.name)
            tmp_dir = tempfile.mkdtemp()
            try:
                cmd = ["rsync"]
                cmd += [
                    "--archive",
                    "--verbose",
                    "--human-readable",
                    "-P",
                    "--force",
                    "--delete",
                    "--compress",
                    f'--partial-dir={os.path.join(self.dir, ".cache/ssync")}',
                ]
                if not slave.is_self():
                    port = slave.ssh_port
                    cmd += ["-e", f"ssh -p {port}"]
                elif not master.is_self():
                    port = master.ssh_port
                    cmd += ["-e", f"ssh -p {port}"]
                if dry_run:
                    cmd += ["--dry-run"]
                cmd += self.backup_parm()
                cmd += self.inex_parm(master, slave, tmp_dir)
                cmd += self.get_source(master)
                cmd += self.get_target(slave)

                logger.debug(" ".join(cmd))
                try:
                    timtools.bash.run(cmd)
                except subprocess.CalledProcessError as error:
                    if error.returncode == 255:
                        raise NotReachableError(slave.name) from error
                    raise error
            except NotReachableError:
                pass
            finally:
                shutil.rmtree(tmp_dir)

    @classmethod
    def backup_parm(cls) -> list:
        """Returns the rsync paramters pertaining to the backup of files"""
        now = dt.datetime.now()
        backup_dir = expanduser(
            join(
                "~/.cache/ssync_backup",
                str(now.year),
                str(now.month),
                str(now.day),
                str(now.strftime("%H%M%S")) + "-" + str(uuid.uuid4()).split("-")[0],
            )
        )
        return ["--backup", "--backup-dir={dir}".format(dir=backup_dir)]

    def inex_parm(self, master: Device, slave: Device, tmp_dir: str) -> list:
        """Retruns the rsync parameters for excluding and including files"""
        infile: str = abspath(join(PROJECT_DIR, "include.txt"))
        exfile: str = abspath(join(PROJECT_DIR, "exclude.txt"))
        limfile: str = abspath(join(PROJECT_DIR, "limited.txt"))
        in2file: str = abspath(join(tmp_dir, "include_rest.txt"))

        with open(in2file, "w") as fobj:
            rules: list[str] = [
                f"{d}/**\n" for d in os.listdir(self.dir) if not d.startswith(".")
            ]
            fobj.writelines(rules)

        parm: list[str] = [
            "--exclude=*.sock",
            f"--include-from={infile}",
            f"--exclude-from={exfile}",
            f"--include-from={in2file}",
            "--exclude=/.*",
        ]

        if slave.sync == "Limited" or master.sync == "Limited":
            parm: list[str] = [
                "--exclude=__pycache__",
                "--exclude=Config/VMs",
                "--exclude=Config/oh-my-zsh/log",
                f"--include-from={limfile}",
                "--exclude=*",
            ]

        return parm

    def get_source(self, master) -> list:
        """Get source parameters of rsync"""
        source: list
        if master.is_self():
            source = [self.dir + "/"]
        else:
            source = [
                "{user}@{ip}:{dir}/".format(
                    user=master.user, ip=master.get_ip(), dir=join("/home", master.user)
                )
            ]
        return source

    def get_target(self, slave) -> list:
        """Get source parameters of rsync"""
        target: list
        if slave.is_self():
            target = [self.dir]
        else:
            target = [
                "{user}@{ip}:{dir}".format(
                    user=slave.user, ip=slave.get_ip(), dir=join("/home", slave.user)
                )
            ]
        return target


def get_active_devices(
    possible_devices: list[Device], limit_sync: bool = True
) -> list[Device]:
    """Returns a list of the devices that are active from within an given list"""
    active_devices_dict: dict[str, Optional[Device]] = {
        dev.name: None for dev in possible_devices
    }

    def test_device(dev: Device):
        if (limit_sync and dev.sync) or (not limit_sync):
            if dev.is_present():
                active_devices_dict[dev.name] = dev

    threads: list[threading.Thread] = []
    for device in possible_devices:
        thread = threading.Thread(target=test_device, args=(device,))
        threads.append(thread)
        thread.start()

    # Wait until all threads have completed
    [t.join() for t in threads]
    active_devices: list[Device] = list(filter(None, active_devices_dict.values()))
    return active_devices


def run():
    """Main executable for ssync"""
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("master", help="Welke computer is de referentie", nargs="?")
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    parser.add_argument("-f", "--from", help="Manuele referentie (heeft --to nodig)")
    parser.add_argument("-t", "--to", help="Maneel doel (heeft --from nodig)")
    parser.add_argument(
        "-l",
        "--limited",
        help="Synchroniseer het minimum aan bestanden",
        action="store_true",
    )
    parser.add_argument(
        "-d", "--dry-run", help="Voer de sync niet echt uit", action="store_true"
    )
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    devices: list = Device.get_devices()
    logger.debug(devices)

    if getattr(args, "from") and args.to:
        # Define both SLAVE and MASTER
        master = Device.get_device(getattr(args, "from").replace(" ", ""))
        slave = [Device.get_device(args.to.replace(" ", ""))]
    elif getattr(args, "from") and not args.to:
        # Define only MASTER
        master = Device.get_device(getattr(args, "from").replace(" ", ""))
        slavename = os.uname().nodename.replace("-tim", "")
        slave = [Device.get_device(slavename)]
    elif not getattr(args, "from") and args.to:
        # Define only SLAVE
        mastername = os.uname().nodename.replace("-tim", "")
        master = Device.get_device(mastername)
        slave = [Device.get_device(args.to.replace(" ", ""))]
    elif args.master:
        master = Device.get_device(args.master)
        slave = [Device.get_device(name) for name in devices if name != args.master]
    else:
        mastername = os.uname().nodename.replace("-tim", "")
        master = Device.get_device(mastername)
        slave = [Device.get_device(name) for name in devices if name != mastername]

    if master in slave:
        raise argparse.ArgumentError(args.master, "Master kan geen slave zijn")

    if args.limited and master.sync:
        master.sync = "Limited"

    if Device.get_device("laptop") in slave:
        answer = input("Ben je zeker dat je naar laptop wilt synchroniseren? (y/N) ")
        if answer.lower() not in ["y", "j"]:
            return

    Sync(master, slave, dry_run=args.dry_run)


if __name__ == "__main__":
    run()
