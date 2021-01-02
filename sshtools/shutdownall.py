#! /usr/bin/python3
"""Script to shutdown all devices simultaneously"""

import argparse
import os
import subprocess
from os.path import expanduser
from time import sleep

from timtools import log

from sshtools.devices import Device
from sshtools.errors import ErrorHandler
from sshtools.sshin import Ssh

PROJECT_DIR = expanduser('~')
logger = log.get_logger(__name__)


class Main:  # pylint: disable=too-few-public-methods
	"""Main executable class for shutdown-all"""

	def __init__(self):
		# Arguments
		parser = argparse.ArgumentParser()
		parser.add_argument(
			'-v', '--verbose',
			help='Geef feedback',
			action='store_true'
		)
		parser.add_argument(
			'-r', '--reboot',
			help='Rebooting instead of shutting down',
			action='store_true'
		)
		parser.add_argument(
			'-s', '--suspend',
			help='suspending instead of shutting down',
			action='store_true'
		)
		args = parser.parse_args()

		log.set_verbose(args.verbose)

		devices: list = Device.get_devices()
		logger.debug(devices)

		master_name = os.uname().nodename.replace('-tim', '')
		names = [name for name in devices if name not in (master_name, 'media', 'imbit')]  # pylint: disable=not-an-iterable
		self.slave = []
		for name in names:
			dev = Device(name)
			try:
				dev.get_ip()
				self.slave.append(dev)
			except ErrorHandler as error:
				logger.critical(error)

		waring_wait: int = 5
		if args.suspend:
			self.send_command(['wall', 'Suspending on order from ' + master_name])
			sleep(waring_wait)
			self.send_command(['sudo', 'systemctl', 'suspend'])
		elif args.reboot:
			self.send_command(['wall', 'Rebooting on order from ' + master_name])
			sleep(waring_wait)
			self.send_command(['sudo', 'shutdown', '-r', 'now'])
		else:
			self.send_command(['wall', 'Shutting down on order from ' + master_name])
			sleep(waring_wait)
			self.send_command(['sudo', 'shutdown', '-h', 'now'])

	def send_command(self, exe: list):
		"""Sends a command to all devices"""
		for slave in self.slave:
			Ssh(slave, exe=' '.join(exe))

		logger.debug(' '.join(exe))
		subprocess.call(exe)


if __name__ == '__main__':
	Main()
