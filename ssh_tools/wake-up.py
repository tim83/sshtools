#!  /usr/bin/python3

import argparse
import os
import subprocess

from timtools import log

from ssh_tools.devices import Device

logger = log.get_logger("ssh_tools.wake-up")


class Wake():
	def __init__(self, dev):

		self.hostname = os.uname().nodename
		self.username = os.environ['USER']
		ip = dev.eth
		mac = dev.emac

		try:
			if ip[:7] == '192.168':
				cmd = ['wol', mac]
			elif ip is not None:
				cmd = ['wol', '-p', dev.ssh_port, '-i', ip, mac]
			else:
				raise ConnectionError()

			logger.debug(' '.join(cmd))
			try:
				response = subprocess.call(cmd)
			except FileNotFoundError:
				response = subprocess.call(['sudo', 'wakeonlan'] + cmd[1:])
			if response != 0:
				print(f'Responsecode from WOL: {response}')
		except ConnectionError:
			logger.critical(f'{dev.hostname} kan niet bereikt worden')


class Main():
	def __init__(self):
		args = self.init_args()
		log.set_verbose(args.verbose)

		devices = Device.get_devices()
		logger.debug(devices)

		target = Device(args.target)
		Wake(target)

	def init_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('target', help='Welke computer is de referentie', nargs='?')
		parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
		args = parser.parse_args()

		return args


if __name__ == '__main__':
	Main()
