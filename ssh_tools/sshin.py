#! /usr/bin/python3

import argparse
import os
import subprocess
import sys

import timtools

from ssh_tools.devices import Device, ConnectionError, ConfigError, DeviceNotPresentError

logger = timtools.log.get_logger("ssh_tools.sshin")


class Ssh:
	def __init__(self, dev, exe: (str, list) = None, mosh: bool = False, copy_id: bool = False, user_override: str = None):
		logger.debug(f'Device: {dev.name} ; Executable: {exe} ; Mosh: {mosh} ; Copy ID: {copy_id}')

		if type(exe) == list:
			exe = ' '.join(exe)

		self.hostname = os.uname().nodename
		self.username = os.environ['USER']  # os.getlogin()
		if user_override:
			user = user_override
		else:
			user = dev.user
		if not dev.ssh:
			raise ConfigError(dev.name)
		try:
			ip = dev.get_ip()
			self.print_header(ip)

			try:
				if copy_id:
					cmd_ci = ['ssh-copy-id', '-p', dev.ssh_port, f'{user}@{ip}']
					logger.debug(' '.join(cmd_ci))

					response_ci = subprocess.call(cmd_ci)
					logger.info(f'SSH-COPY-ID exited with code {response_ci}')
				if mosh:
					cmd = ['mosh', f'{user}@{ip}']
				else:
					cmd = ['ssh', '-t', '-p', dev.ssh_port, f'{user}@{ip}']

				if exe:
					cmd += [exe]

				logger.debug(' '.join(cmd))
				timtools.bash.run(cmd)
			except ConnectionError:
				pass
			except subprocess.CalledProcessError as e:
				if e.returncode != 255:
					raise e

			self.print_footer()

		except DeviceNotPresentError:
			relay = dev.get_relay()
			if relay:
				Ssh(relay, exe=["python3 -m ssh_tools.sshin"] + [f"\"{arg}\"" for arg in sys.argv[1:]], mosh=mosh, copy_id=copy_id)

	def print_header(self, ip):
		# os.system('clear')
		twidth = self.get_terminal_columns()

		print(f'Connecting to {ip} ...\n')
		print('-' * twidth + '\n')

	@staticmethod
	def get_terminal_columns():
		try:
			return os.get_terminal_size().columns
		except OSError:
			return 80

	def print_footer(self):
		twidth = self.get_terminal_columns()
		print('\n' + '-' * twidth + '\n')


class Main:
	def __init__(self):
		args = self.init_args()
		timtools.log.set_verbose(args.verbose)

		devices = Device.get_devices()
		logger.debug(devices)

		target = Device(args.target)

		if args.mosh:
			use_mosh = True
		elif args.ssh:
			use_mosh = False
		# elif args.command:
		# 	use_mosh = False
		else:
			use_mosh = target.mosh
		Ssh(target, exe=args.command, mosh=use_mosh, copy_id=args.copy_id, user_override=args.user)

	def init_args(self):
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

		return args


if __name__ == '__main__':
	Main()
