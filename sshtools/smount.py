#! /usr/bin/python3
"""Mounts a device using sftp"""

import argparse
import os
import subprocess

from timtools import log

from sshtools.devices import Device
from sshtools.errors import ConfigError, NotReachableError, DeviceNotPresentError, NotEmptyError
from sshtools.sshin import Ssh

logger = log.get_logger(__name__)


class Mount:
	"""Mounts a source directory of a device on mountpoint"""

	def __init__(self, device: Device, src: str, mountpoint: str, open_mountpoint: bool = False,
			be_root: bool = False):
		logger.debug('Device: %s ; Source %s ; Mountpoint %s', device, src, mountpoint)

		self.hostname = os.uname().nodename
		self.username = os.environ['USER']
		if not device.ssh:
			raise ConfigError(device.name)
		try:
			ip_addr = device.get_ip()

			try:
				os.makedirs(mountpoint, exist_ok=True)
				if len(os.listdir(mountpoint)) > 0:
					raise NotEmptyError(mountpoint)

				cmd = [
					'mount',
					'-t', 'fuse.sshfs',
					'-o', 'user,_netdev,reconnect,uid=1000,gid=1000,allow_other',
					f'{device.user}@{ip_addr}:{src}', f"{mountpoint}"
				]
				if be_root:
					cmd.insert(0, "sudo")

				logger.debug(' '.join(cmd))
				response = subprocess.call(cmd)
				if response != 0:
					print(f'Responsecode from SSH: {response}')
				else:
					if open_mountpoint:
						subprocess.call(["xdg-open", mountpoint])
			except NotReachableError:
				logger.critical(device.name)

		except DeviceNotPresentError:
			relay = device.get_relay()
			dest: str
			if mountpoint[0] == '/':
				dest = mountpoint[1:]
			else:
				dest = mountpoint
			relay_mount = os.path.join("/tmp/smount", device.name, dest)
			Ssh(relay, exe=["python3", "-m", "sshtools.smount", device.name, f"\"{src}\"",
				f"\"{relay_mount}\""])
			Mount(relay, relay_mount, mountpoint)

	@classmethod
	def print_header(cls, ip_addr: str):
		"""Prints a header to the terminal"""
		os.system('clear')
		try:
			twidth = os.get_terminal_size().columns

			print(f'Connecting to {ip_addr} ...\n')
			print('-' * twidth + '\n')
		except OSError:
			pass

	@classmethod
	def print_footer(cls):
		"""Prints a footer to the terminal"""
		twidth = os.get_terminal_size().columns
		print('\n' + '-' * twidth + '\n')


def main():
	"""Main executable class for smount"""
	parser = argparse.ArgumentParser()
	parser.add_argument('target', help='Welke computer is de referentie')
	parser.add_argument('source', help='Locatie op taget die gemount moet worden', nargs='?',
		default="/home/tim")
	parser.add_argument('mountpoint', help='Mountpoint')
	parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
	parser.add_argument('-r', '--root', help='Koppel de locatie aan als ROOT', action='store_true')
	parser.add_argument('-o', '--open', help='Open het mountpoint', action='store_true')
	args = parser.parse_args()

	log.set_verbose(args.verbose)

	devices = Device.get_devices()
	logger.debug(devices)

	target = Device.get_device(args.target)
	source = args.source
	mountpoint = args.mountpoint

	Mount(target, source, mountpoint, open_mountpoint=args.open, be_root=args.root)


if __name__ == "__main__":
	main()
