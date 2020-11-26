#! /usr/bin/python3
"""Module to obtain the IP adress of a device"""

import argparse

import timtools

from devices import Device

logger = timtools.log.get_logger('ssh-tools.getip')


def get_ip(target: str) -> str:
	"""Return the IP address of a target device"""
	dev = Device(target)
	ip_addr = dev.get_ip()
	return ip_addr


def get_string(target: str) -> str:
	"""Return the full address of the user on the device"""
	dev = Device(target)
	ip_addr = dev.get_ip()
	return f"{dev.user}@{ip_addr}"


if __name__ == "__main__":
	# Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('target', help='Computer voor wie het ip adres moet worden bepaald', nargs='?')
	parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
	parser.add_argument('-s', '--ssh-string', help='Geeft de volledige string voor SSH ([USER]@[IP])', action='store_true')
	args = parser.parse_args()

	timtools.log.set_verbose(args.verbose)

	if args.ssh_string:
		print(get_string(args.target))
	else:
		print(get_ip(args.target))
