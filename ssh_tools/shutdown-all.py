#! /usr/bin/python3

import argparse
import os
import subprocess
from configparser import ConfigParser, NoSectionError
from os.path import join, expanduser
from time import sleep

from timtools import log
# from sshin import Device, Ssh

PROJECT_DIR = expanduser('~')  # dirname(__file__)
logger = log.get_logger("ssh_tools.shutdown-all")

# Errors


class ConnectionError(Exception):
	def __init__(self, message):
		super().__init__(message)


class DeviceNotFoundError(Exception):
	def __init__(self, message):
		super().__init__('Device {name} not found'.format(name=message))


# Definitions


class Device():
	def __init__(self, name, config):
		self.get_config(name, config)
		self.ip = None

	def get_config(self, name, config):
		try:
			self.hostname = config.get(name, 'hostname')
			self.user = config.get(name, 'user', fallback='tim')
			self.wlan = config.get(name, 'wlan', fallback=None)
			self.eth = config.get(name, 'eth', fallback=None)
		except NoSectionError:
			raise DeviceNotFoundError(name)

	def get_ip(self):
		if self.ip:
			return self.ip
		else:
			for ip in self.eth, self.wlan:
				response = os.system(f'ping -c 1 {ip} > /dev/null')
				if response == 0:
					self.ip = f'{self.user}@{ip}'
					return self.ip
			else:
				raise ConnectionError(
					'Kon {target} niet bereiken'.format(target=self.hostname))

	def __repr__(self):
		return '<Device({name})>'.format(name=self.hostname)


class Ssh():
	def __init__(self, dev, exe=None):
		self.hostname = os.uname().nodename
		ip = dev.get_ip()
		# twith = os.get_terminal_size().columns

		print(f'Connecting to {ip} ...\n')

		try:
			cmd = ['ssh', '-t', ip]

			if exe:
				cmd += [exe]

			logger.debug(' '.join(cmd))
			subprocess.call(cmd)
		except ConnectionError:
			logger.critical(f'{dev.hostname} kan niet bereikt worden')


class Main():
	def __init__(self):
		args = self.init_args()
		log.set_verbose(args.verbose)

		self.config, devices = self.get_devices()
		logger.debug(devices)

		mastername = os.uname().nodename.replace('-tim', '')
		names = [name for name in devices if name not in (
			mastername, 'media', 'imbit')]
		self.slave = []
		for n in names:
			dev = Device(n, self.config)
			try:
				dev.get_ip()
				self.slave.append(dev)
			except Exception as e:
				logger.critical(e)

		# ~ logger.info('Controlling ' + ', '.join(self.slave))

		if args.suspend:
			self.send_command(
				['wall', 'Suspending on order from ' + mastername])
			sleep(5)
			self.send_command(['sudo', 'systemctl', 'suspend'])
		elif args.reboot:
			self.send_command(
				['wall', 'Rebooting on order from ' + mastername])
			sleep(5)
			self.send_command(['sudo', 'shutdown', '-r', 'now'])
		else:
			self.send_command(
				['wall', 'Shutting down on order from ' + mastername])
			sleep(5)
			self.send_command(['sudo', 'shutdown', '-h', 'now'])

	def send_command(self, exe):
		for s in self.slave:
			Ssh(s, exe=' '.join(exe))

		logger.debug(' '.join(exe))
		subprocess.call(exe)

	def get_devices(self):
		config = ConfigParser()
		config.read([
			join(PROJECT_DIR, 'devices.ini'),
			expanduser('/ssh_tools/devices.ini')
		])

		devices = config.sections()

		return config, devices

	def init_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-v', '--verbose',
			help='Geef feedback', action='store_true')
		parser.add_argument(
			'-r', '--reboot', help='Rebooting instead of shutting down', action='store_true')
		parser.add_argument(
			'-s', '--suspend', help='suspending instead of shutting down', action='store_true')
		args = parser.parse_args()

		return args


if __name__ == '__main__':
	Main()
