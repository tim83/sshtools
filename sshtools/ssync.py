#! /usr/bin/python3
"""Syncs devices over LAN"""

import argparse
import datetime as dt
import os
import uuid
import subprocess
from os.path import abspath, dirname, expanduser, join
from typing import List

import timtools.bash
import timtools.log

from sshtools.devices import Device
from sshtools.errors import NotReachableError

PROJECT_DIR: str = dirname(__file__)
TMP_DIR: str = "/tmp"
logger = timtools.log.get_logger(__name__)


class Sync:
	"""Sync devices"""
	dir: str
	username: str
	hostname: str

	def __init__(self, master, slaves, dry_run=False):
		self.hostname = os.uname().nodename
		self.username = os.environ['USER']
		self.dir = expanduser('~')

		for slave in slaves:
			if not slave.sync or not slave.is_present():
				continue
			print()
			print(master.name + ' -> ' + slave.name)
			try:
				cmd = ['rsync']
				cmd += [
					'--archive',
					'--verbose',
					'--human-readable',
					'-P',
					'--force',
					'--delete',
					'--compress',
					f'--partial-dir={os.path.join(self.dir, ".cache/ssync")}'
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
				cmd += self.inex_parm(master, slave)
				cmd += self.get_source(master)
				cmd += self.get_target(slave)

				logger.debug(' '.join(cmd))
				try:
					timtools.bash.run(cmd)
				except subprocess.CalledProcessError as error:
					if error.returncode == 255:
						raise NotReachableError(slave.name) from error
					raise error
			except NotReachableError:
				pass

	@classmethod
	def backup_parm(cls) -> list:
		"""Returns the rsync paramters pertaining to the backup of files"""
		now = dt.datetime.now()
		backup_dir = expanduser(join(
			'~/.cache/ssync_backup',
			str(now.year), str(now.month), str(now.day),
			str(now.strftime("%H%M%S")) + "-" + str(uuid.uuid4()).split('-')[0]
		))
		return ['--backup', '--backup-dir={dir}'.format(dir=backup_dir)]

	def inex_parm(self, master: Device, slave: Device) -> list:
		"""Retruns the rsync parameters for excluding and including files"""
		infile: str = abspath(join(PROJECT_DIR, 'include.txt'))
		exfile: str = abspath(join(PROJECT_DIR, 'exclude.txt'))
		limfile: str = abspath(join(PROJECT_DIR, 'limited.txt'))
		in2file: str = abspath(join(TMP_DIR, 'include_rest.txt'))

		with open(in2file, "w") as fobj:
			rules: List[str] = [
				f"{d}/**\n"
				for d in os.listdir(self.dir)
				if not d.startswith(".")
			]
			fobj.writelines(rules)

		parm: list = [
			"--exclude=*.sock",
			f"--include-from={infile}",
			f'--exclude-from={exfile}',
			f"--include-from={in2file}",
			"--exclude=/.*"
		]

		if slave.sync == 'Limited' or master.sync == 'Limited':
			parm: list = [
				'--exclude=__pycache__',
				'--exclude=Config/VMs',
				'--exclude=Config/oh-my-zsh/log',
				f'--include-from={limfile}',
				'--exclude=*'
			]

		return parm

	def get_source(self, master) -> list:
		"""Get source parameters of rsync"""
		source: list
		if master.is_self():
			source = [self.dir + '/']
		else:
			source = ['{user}@{ip}:{dir}/'.format(
				user=master.user,
				ip=master.get_ip(),
				dir=join('/home', master.user)
			)]
		return source

	def get_target(self, slave) -> list:
		"""Get source parameters of rsync"""
		target: list
		if slave.is_self():
			target = [self.dir]
		else:
			target = ['{user}@{ip}:{dir}'.format(
				user=slave.user,
				ip=slave.get_ip(),
				dir=join('/home', slave.user)
			)]
		return target


def run():
	"""Main executable for ssync"""
	# Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('master', help='Welke computer is de referentie', nargs='?')
	parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
	parser.add_argument('-f', '--from', help='Manuele referentie (heeft --to nodig)')
	parser.add_argument('-t', '--to', help='Maneel doel (heeft --from nodig)')
	parser.add_argument(
		'-l', '--limited',
		help='Synchroniseer het minimum aan bestanden',
		action='store_true'
	)
	parser.add_argument(
		'-d', '--dry-run',
		help='Voer de sync niet echt uit',
		action='store_true'
	)
	args = parser.parse_args()

	timtools.log.set_verbose(args.verbose)

	devices: list = Device.get_devices()
	logger.debug(devices)

	if getattr(args, 'from') and args.to:
		# Define both SLAVE and MASTER
		master = Device.get_device(getattr(args, 'from').replace(' ', ''))
		slave = [Device.get_device(args.to.replace(' ', ''))]
	elif getattr(args, 'from') and not args.to:
		# Define only MASTER
		master = Device.get_device(getattr(args, 'from').replace(' ', ''))
		slavename = os.uname().nodename.replace('-tim', '')
		slave = [Device.get_device(slavename)]
	elif not getattr(args, 'from') and args.to:
		# Define only SLAVE
		mastername = os.uname().nodename.replace('-tim', '')
		master = Device.get_device(mastername)
		slave = [Device.get_device(args.to.replace(' ', ''))]
	elif args.master:
		master = Device.get_device(args.master)
		slave = [Device.get_device(name) for name in devices if name != args.master]
	else:
		mastername = os.uname().nodename.replace('-tim', '')
		master = Device.get_device(mastername)
		slave = [Device.get_device(name) for name in devices if name != mastername]

	if master in slave:
		raise argparse.ArgumentError(args.master, 'Master kan geen slave zijn')

	if args.limited and master.sync:
		master.sync = 'Limited'

	logger.info("%s -> %s", master.hostname, ', '.join([s.hostname for s in slave]))

	Sync(master, slave, dry_run=args.dry_run)


if __name__ == '__main__':
	run()
