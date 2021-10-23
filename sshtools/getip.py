#! /usr/bin/python3
"""Module to obtain the IP adress of a device"""

import argparse

import timtools.log

from sshtools.devices import Device

logger = timtools.log.get_logger('ssh-tools.getip')


def get_string(target: Device) -> str:
	"""Return the full address of the user on the device"""
	ip_addr = target.ip_addr
	return f"{target.user}@{ip_addr}"


def run():
	# Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'target',
		help='Computer voor wie het ip adres moet worden bepaald',
		nargs='?'
	)
	parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
	parser.add_argument(
		'-s', '--ssh-string',
		help='Geeft de volledige string voor SSH ([USER]@[IP])',
		action='store_true'
	)
	parser.add_argument(
		'-i', '--ip',
		help='Gebruik alleen IP adressen en geen DNS of hostnamen',
		action='store_true'
	)
	args = parser.parse_args()

	timtools.log.set_verbose(args.verbose)

	target: Device = Device.get_device(args.target)

	if args.ip:
		target.get_ip(strict_ip=True)

	if args.ssh_string:
		print(get_string(target))
	else:
		print(target.ip_addr)


if __name__ == "__main__":
	run()
