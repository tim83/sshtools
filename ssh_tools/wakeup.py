#!  /usr/bin/python3
"""Module to wake up devices using wake on lan"""

import argparse
import subprocess

from timtools import log

from devices import Device

logger = log.get_logger(__name__)


def wake(device: Device):
	"""Wake up a device"""
	ip_addr: str = device.eth
	mac_addr: str = device.emac

	try:
		cmd: list
		if ip_addr[:7] == '192.168':
			cmd = ['wol', mac_addr]
		elif ip_addr is not None:
			cmd = ['wol', '-p', device.ssh_port, '-i', ip_addr, mac_addr]
		else:
			raise ConnectionError()

		logger.debug(' '.join(cmd))

		response: int
		try:
			response = subprocess.call(cmd)
		except FileNotFoundError:
			response = subprocess.call(['sudo', 'wakeonlan'] + cmd[1:])

		if response != 0:
			print(f'Responsecode from WOL: {response}')
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

	target = Device(args.target)
	wake(target)


if __name__ == '__main__':
	main()
