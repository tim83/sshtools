#! /usr/bin/python3

import argparse
import os
import subprocess

from timtools import log

from ssh_tools.devices import Device, ConnectionError, ConfigError, DeviceNotPresentError, ErrorHandler
from ssh_tools.sshin import Ssh

logger = log.get_logger("ssh_tools.smount")


# ~ PROJECT_DIR = dirname(__file__)

class NotEmptyError(ErrorHandler):
	def __init__(self, mountpoint):
		super().__init__(f'Mountpoint {mountpoint} is not empty.')


class Mount():
	def __init__(self, dev, src, mountpoint, open=False):
		logger.debug(f'Device: {dev.name} ; Source {src} ; Mountpoint {mountpoint}')

		self.hostname = os.uname().nodename
		self.username = os.environ['USER']  # os.getlogin()
		if not dev.ssh:
			raise ConfigError(dev.name)
		try:
			ip = dev.get_ip()
			relay = None

			try:
				os.makedirs(mountpoint, exist_ok=True)
				if len(os.listdir(mountpoint)) > 0:
					raise NotEmptyError(mountpoint)
				else:
					cmd = ['mount', '-t', 'fuse.sshfs', '-o', 'user,_netdev,reconnect,uid=1000,gid=1000,allow_other', f'{dev.user}@{ip}:{src}', f"{mountpoint}"]
					logger.debug(' '.join(cmd))
					response = subprocess.call(cmd)
					if response != 0:
						print(f'Responsecode from SSH: {response}')
					else:
						if open:
							subprocess.call(["xdg-open", mountpoint])
			except ConnectionError:
				logger.critical(dev.name)

		except DeviceNotPresentError:
			relay = dev.get_relay()
			if mountpoint[0] == '/':
				d = mountpoint[1:]
			else:
				d = mountpoint
			relay_mount = os.path.join("/tmp/smount", dev.name, d)
			Ssh(relay, exe=["python3", "-m", "ssh_tools.smount", dev.name, f"\"{src}\"", f"\"{relay_mount}\""])
			Mount(relay, relay_mount, mountpoint)

	def print_header(self, ip):
		os.system('clear')
		try:
			twidth = os.get_terminal_size().columns

			print(f'Connecting to {ip} ...\n')
			print('-' * twidth + '\n')
		except OSError:
			pass

	def print_footer(self):
		twidth = os.get_terminal_size().columns
		print('\n' + '-' * twidth + '\n')


class Main():
	def __init__(self):
		args = self.init_args()
		log.set_verbose(args.verbose)

		devices = Device.get_devices()
		logger.debug(devices)

		target = Device(args.target)
		source = args.source
		mountpoint = args.mountpoint

		Mount(target, source, mountpoint, open=args.open)

	def init_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('target', help='Welke computer is de referentie')
		parser.add_argument('source', help='Locatie op taget die gemount moet worden', nargs='?', default="/home/tim")
		parser.add_argument('mountpoint', help='Mountpoint')
		parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
		parser.add_argument('-o', '--open', help='Open het mountpoint', action='store_true')
		args = parser.parse_args()

		return args


if __name__ == '__main__':
	Main()
