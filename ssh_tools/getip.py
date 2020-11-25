#! /usr/bin/python3

import argparse

import timtools

from ssh_tools.devices import Device

logger = timtools.log.get_logger('ssh-tools.getip')


def get_ip(target):
	dev = Device(target)
	ip = dev.get_ip()
	return ip


def get_string(target):
	dev = Device(target)
	ip = dev.get_ip()
	return f"{dev.user}@{ip}"


class Main():
	def __init__(self):
		args = self.init_args()
		timtools.log.set_verbose(args.verbose)

		if args.ssh_string:
			string = get_string(args.target)
			print(string)
		else:
			ip = get_ip(args.target)
			print(ip)

	def init_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('target', help='Computer voor wie het ip adres moet worden bepaald', nargs='?')
		parser.add_argument('-v', '--verbose', help='Geef feedback', action='store_true')
		parser.add_argument('-s', '--ssh-string', help='Geeft de volledige string voor SSH ([USER]@[IP])', action='store_true')
		args = parser.parse_args()

		return args


if __name__ == '__main__':
	Main()
