#! /usr/bin/python3
"""Syncs devices over LAN"""

import argparse
import datetime as dt
import os
import subprocess
from os.path import abspath, dirname, expanduser, join

import timtools.bash
import timtools.log

from sshtools.devices import Device
from sshtools.errors import NotReachableError

PROJECT_DIR = dirname(__file__)
logger = timtools.log.get_logger(__name__)


class Sync:
	"""Sync devices"""

	def __init__(self, master, slaves):
		self.hostname = os.uname().nodename
		self.username = os.environ['USER']
		self.dir = expanduser('~')

		for slave in slaves:
			if not slave.sync or not slave.present:
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
					cmd += [f"-e \'ssh -p {port}\'"]
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
		backup_dir = join('/var/tmp/sync', str(now.year), str(now.month), str(now.day))
		return ['--backup', '--backup-dir={dir}'.format(dir=backup_dir)]

	@classmethod
	def inex_parm(cls, master: Device, slave: Device) -> list:
		"""Retruns the rsync parameters for excluding and including files"""
		infile: str = abspath(join(PROJECT_DIR, 'include.txt'))
		exfile: str = abspath(join(PROJECT_DIR, 'exclude.txt'))
		limfile: str = abspath(join(PROJECT_DIR, 'limited.txt'))

		parm: list = [
			"--exclude=*.sock",
			f"--include-from={infile}",
			f'--exclude-from={exfile}',
			"--exclude=.*"
		]

		if slave.sync == 'Limited' or master.sync == 'Limited':
			parm: list = [
				'--exclude=__pycache__',
				'--exclude=Documenten/pc/config/VMs',
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


def main():
	"""Main executable for ssync"""
	# Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('master', help='Welke computer is de referentie', nargs='?')
	parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
	parser.add_argument('-f', '--from', help='Manuele referentie (heeft --to nodig)')
	parser.add_argument('-t', '--to', help='Maneel doel (heeft --from nodig)')
	parser.add_argument('-l', '--limited', help='Synchroniseer het minimum aan bestanden', action='store_true')
	args = parser.parse_args()

	timtools.log.set_verbose(args.verbose)

	devices: list = Device.get_devices()
	logger.debug(devices)

	if getattr(args, 'from') and args.to:
		# Define both SLAVE and MASTER
		master = Device(getattr(args, 'from').replace(' ', ''))
		slave = [Device(args.to.replace(' ', ''))]
	elif getattr(args, 'from') and not args.to:
		# Define only MASTER
		master = Device(getattr(args, 'from').replace(' ', ''))
		slavename = os.uname().nodename.replace('-tim', '')
		slave = [Device(slavename)]
	elif not getattr(args, 'from') and args.to:
		# Define only SLAVE
		mastername = os.uname().nodename.replace('-tim', '')
		master = Device(mastername)
		slave = [Device(args.to.replace(' ', ''))]
	elif args.master:
		master = Device(args.master)
		slave = [Device(name) for name in devices if name != args.master]  # pylint: disable=not-an-iterable
	else:
		mastername = os.uname().nodename.replace('-tim', '')
		master = Device(mastername)
		slave = [Device(name) for name in devices if name != mastername]  # pylint: disable=not-an-iterable

	if master in slave:
		raise argparse.ArgumentError(args.master, 'Master kan geen slave zijn')

	if args.limited and master.sync:
		master.sync = 'Limited'

	logger.info("%s -> %s", master.hostname, ', '.join([s.hostname for s in slave]))

	Sync(master, slave)


if __name__ == '__main__':
	main()
