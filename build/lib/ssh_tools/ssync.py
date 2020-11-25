#! /usr/bin/python3

import argparse
import datetime as dt
import os
import subprocess
from os.path import join, expanduser, abspath, dirname

import timtools

from ssh_tools.devices import Device, ConnectionError

PROJECT_DIR = dirname(__file__)
logger = timtools.log.get_logger("ssh_tools.ssync")


class Sync:
	def __init__(self, master, slave):
		self.hostname = os.uname().nodename
		self.username = os.environ['USER']
		self.dir = expanduser('~')

		for s in slave:
			if not s.sync or not s.present:
				continue
			print()
			print(master.name + ' -> ' + s.name)
			try:
				cmd = ['rsync'] + ['--archive', '-v', '-h', '-P', '--force', '--delete'] + self.backup_parm() + self.inex_parm(master, s) + self.get_source(master) + self.get_target(s)

				logger.debug(' '.join(cmd))
				try:
					print(cmd)
					timtools.bash.run(cmd)
				except subprocess.CalledProcessError as e:
					if e.returncode == 255:
						raise ConnectionError(s.name)
					else:
						raise e
			except ConnectionError:
				pass

	def backup_parm(self):
		now = dt.datetime.now()
		backup_dir = join('/var/tmp/sync', str(now.year), str(now.month), str(now.day))
		return ['--backup', '--backup-dir={dir}'.format(dir=backup_dir)]

	def inex_parm(self, master: Device, slave: Device) -> list:
		infile: str = abspath(join(PROJECT_DIR, 'include.txt'))
		exfile: str = abspath(join(PROJECT_DIR, 'exclude.txt'))
		limfile: str = abspath(join(PROJECT_DIR, 'limited.txt'))

		parm: list = ["--exclude=*.sock", f"--include-from={infile}", f'--exclude-from={exfile}']
		# home_files: list = [f for f in os.listdir(os.path.expanduser("~")) if not f.startswith('.')]
		# parm += " ".join([f"--include=\"{file}\"" for file in home_files])
		parm += ["--exclude=.*"]

		if slave.sync == 'Limited' or master.sync == 'Limited':
			parm: list = ['--exclude=__pycache__', f'--include-from={limfile}', '--exclude=*']

		return parm

	def get_source(self, master):
		if self.hostname == master.hostname:
			return [self.dir + '/']
		else:
			return ['{user}@{ip}:{dir}/'.format(user=master.user, ip=master.get_ip(), dir=join('/home', master.user))]

	def get_target(self, slave):
		if self.hostname == slave.hostname:
			return [self.dir]
		else:
			return ['{user}@{ip}:{dir}'.format(user=slave.user, ip=slave.get_ip(), dir=join('/home', slave.user))]


class Main:
	def __init__(self):
		args = self.init_args()
		timtools.log.set_verbose(args.verbose)

		devices = Device.get_devices()
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
			slave = [Device(name) for name in devices if name != args.master]
		else:
			mastername = os.uname().nodename.replace('-tim', '')
			master = Device(mastername)
			slave = [Device(name) for name in devices if name != mastername]

		if master in slave:
			raise argparse.ArgumentError(args.master, 'Master kan geen slave zijn')

		logger.info(master.hostname + ' -> ' + ', '.join([s.hostname for s in slave]))

		Sync(master, slave)

	def init_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('master', help='Welke computer is de referentie', nargs='?')
		parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
		parser.add_argument('-f', '--from', help='Manuele referentie (heeft --to nodig)')
		parser.add_argument('-t', '--to', help='Maneel doel (heeft --from nodig)')
		args = parser.parse_args()

		return args


if __name__ == '__main__':
	Main()
