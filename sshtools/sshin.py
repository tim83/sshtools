#! /usr/bin/python3
"""Module to ssh into a device"""

import argparse
import os
import subprocess
import sys

import timtools.log

from ssh_tools.devices import Device
from ssh_tools.errors import ConfigError, DeviceNotPresentError

logger = timtools.log.get_logger(__name__)


class Ssh:
	"""Class to ssh into a device"""

	def __init__(self, dev, exe: (str, list) = None, mosh: bool = False, copy_id: bool = False):
		logger.debug('Device: %s ; Executable: %s ; Mosh: %s ; Copy ID: %s', dev, exe, mosh, copy_id)

		if isinstance(exe, list):
			exe = ' '.join(exe)

		self.hostname = os.uname().nodename
		self.username = os.environ['USER']  # os.getlogin()
		user = dev.user
		if not dev.ssh:
			raise ConfigError(dev.name)
		try:
			ip_addr = dev.get_ip()
			self.print_header(ip_addr)

			try:
				if copy_id:
					cmd_ci = ['ssh-copy-id', '-p', str(dev.ssh_port), f'{user}@{ip_addr}']
					logger.debug(' '.join(cmd_ci))

					response_ci = timtools.bash.run(cmd_ci)
					logger.info('SSH-COPY-ID exited with code %s', response_ci)
				if mosh:
					cmd = ['mosh', f'{user}@{ip_addr}']
				else:
					cmd = ['ssh', '-t', '-p', str(dev.ssh_port), f'{user}@{ip_addr}']

				if exe:
					cmd += [exe]

				logger.debug(' '.join(cmd))
				timtools.bash.run(cmd)
			except ConnectionError:
				pass
			except subprocess.CalledProcessError as error:
				if error.returncode != 255:
					raise error

			self.print_footer()

		except DeviceNotPresentError:
			relay = dev.get_relay()
			if relay:
				Ssh(relay, exe=["python3 -m ssh_tools.sshin"] + [f"\"{arg}\"" for arg in sys.argv[1:]], mosh=mosh, copy_id=copy_id)

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

	target = Device(args.target)

	if args.mosh:
		use_mosh = True
	elif args.ssh:
		use_mosh = False
	else:
		use_mosh = target.mosh
	Ssh(target, exe=args.command, mosh=use_mosh, copy_id=args.copy_id)


if __name__ == '__main__':
	main()
