#!  /usr/bin/python3
"""Module to wake up devices using wake on lan"""

import argparse
import subprocess

from timtools import log, bash

from sshtools.devices import Device

logger = log.get_logger(__name__)


def wake(device: Device):
	"""Wake up a device"""
	ip_addr: str = device.eth[0]
	mac_addr: str = device.emac

	try:
		cmd: list
		if ip_addr[:7] == '192.168':
			cmd = ['wol', mac_addr]
		elif ip_addr is not None:
			cmd = ['wol', '-p', device.ssh_port, '-i', ip_addr, mac_addr]
		else:
			raise ConnectionError()

		logger.debug(cmd)

		try:
			bash.run(cmd)
		except subprocess:
			bash.run(['sudo', 'wakeonlan'] + cmd[1:])

	except ConnectionError:
		logger.critical('%s kan niet bereikt worden', device.hostname)


def main():
	"""Main executable for wake-up"""
	parser = argparse.ArgumentParser()
	parser.add_argument('target', help='Welke computer is de referentie', nargs='?')
	parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
	args = parser.parse_args()
	log.set_verbose(args.verbose)

	devices = Device.get_devices()
	logger.debug(devices)

	target = Device.get_device(args.target)
	wake(target)


if __name__ == '__main__':
	main()
