#! /usr/bin/python3
"""Module to obtain the IP adress of a device"""

import argparse

import timtools.log

import sshtools.errors
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
		nargs='*'
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

	target_names: list[str]
	if len(args.target) == 0:
		# target_names = Device.get_devices()
		target_names = ["laptop", "thinkcentre", "fujitsu", "probook", "serverpi", "camerapi"]
	else:
		target_names = args.target

	for target_name in target_names:
		target: Device = Device.get_device(target_name)

		if args.ip:
			target.get_ip(strict_ip=True)

		ip_string: str
		try:
			if args.ssh_string:
				ip_string = get_string(target)
			else:
				ip_string = target.ip_addr
		except (sshtools.errors.NotReachableError, sshtools.errors.DeviceNotPresentError):
			ip_string = "none"

		if len(target_names) == 1:
			print(ip_string)
		else:
			print(f"{target.name}:\t{ip_string}")


if __name__ == "__main__":
	run()
