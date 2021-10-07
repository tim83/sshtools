#! /usr/bin/python3
"""Module to ssh into a device"""

import argparse
import os
import subprocess
import sys

import timtools.log

from sshtools.devices import Device
from sshtools.errors import ConfigError, DeviceNotPresentError

logger = timtools.log.get_logger(__name__)


class Ssh:
	"""Class to ssh into a device"""

	def __init__(
			self,
			dev: Device,
			exe: (str, list) = None,
			mosh: bool = False,
			copy_id: bool = False,
			connect: bool = True
	):
		if connect:
			logger.debug('Device: %s ; Executable: %s ; Mosh: %s ; Copy ID: %s', dev.hostname, exe, mosh, copy_id)
		else:
			logger.debug('Device: %s', dev.hostname)

		self.device: Device = dev
		self.hostname: str = os.uname().nodename
		self.username: str = os.environ['USER']  # os.getlogin()

		if connect:
			self.connect(exe=exe, copy_id=copy_id, mosh=mosh)

	def connect(
			self,
			ip_addr: str = None,
			exe: (str, list) = None,
			ssh_port: str = None,
			copy_id: bool = False,
			mosh: bool = False,
	):

		user = self.device.user
		if not self.device.ssh:
			raise ConfigError(self.device.name)

		if isinstance(exe, list):
			exe = ' '.join(exe)

		if ip_addr is None:
			ip_addr = self.device.get_ip()
		else:
			ip_addr = ip_addr

		if ssh_port is None:
			ssh_port = str(self.device.ssh_port)
		else:
			ssh_port = ssh_port

		self.print_header(ip_addr)

		try:
			if copy_id:
				cmd_ci = ['ssh-copy-id', '-p', ssh_port, f'{user}@{ip_addr}']
				logger.debug(' '.join(cmd_ci))

				response_ci = timtools.bash.run(cmd_ci)
				logger.info('SSH-COPY-ID exited with code %s', response_ci)
			if mosh and self.device.is_local():
				cmd = ['mosh', f'{user}@{ip_addr}']
			else:
				cmd = ['ssh', '-t', '-p', ssh_port, f'{user}@{ip_addr}']

			if exe:
				cmd += [exe]

			logger.debug(' '.join(cmd))
			timtools.bash.run(cmd, passable_exit_codes=[255, 100, 127])
		except ConnectionError:
			pass

			self.print_footer()

		except DeviceNotPresentError:
			relay = self.device.get_relay()
			if relay:
				Ssh(
					relay,
					exe=["python3 -m sshtools.sshin"] + [f"\"{arg}\"" for arg in sys.argv[1:]],
					mosh=mosh, copy_id=copy_id
				)

	def print_header(self, ip_addr: str):
		"""Prints a header to the terminal"""
		twidth = self.get_terminal_columns()

		print(f'Connecting to {ip_addr} ...\n')
		print('-' * twidth + '\n')

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
		print('\n' + '-' * twidth + '\n')


def main():
	"""Main executable for sshin"""
	logger.debug(sys.argv)
	parser = argparse.ArgumentParser()
	parser.add_argument('target', help='Welke computer is de referentie')
	parser.add_argument('-c', '--command', help='Uit te voeren commando')
	parser.add_argument('-u', '--user', help='Login als deze gebruiker, in plaats van de standaard gebruiker')
	parser.add_argument('-i', '--copy-id', help='Voert ssh-copy-id uit voor de verbinden', action='store_true')
	parser.add_argument('-m', '--mosh', help='Gebruik MOSH in plaats van SSH', action='store_true')
	parser.add_argument('-s', '--ssh', help='Gebruik MOSH in plaats van SSH', action='store_true')
	parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
	args = parser.parse_args()
	logger.debug(args)

	timtools.log.set_verbose(args.verbose)

	devices = Device.get_devices()
	logger.debug(devices)

	target = Device.get_device(args.target)

	if args.mosh:
		use_mosh = True
	elif args.ssh:
		use_mosh = False
	else:
		use_mosh = target.mosh
	Ssh(target, exe=args.command, mosh=use_mosh, copy_id=args.copy_id)


if __name__ == '__main__':
	main()
