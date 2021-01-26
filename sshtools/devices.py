#! /usr/bin/python3
"""Classes for managing devices used by other files"""

import os
import socket
import subprocess
from configparser import ConfigParser, NoSectionError, RawConfigParser
from collections import OrderedDict
from os.path import dirname, expanduser, join
from typing import List

import psutil
from timtools import bash
from timtools.log import get_logger

from sshtools.errors import \
	DeviceNotFoundError, \
	DeviceNotPresentError, \
	ErrorHandler, \
	NetworkError, \
	NotReachableError

project_dir = dirname(__file__)
logger = get_logger(__name__)


def get_ips():
	"""Get the IPs that the current device has assigned"""
	interfaces = psutil.net_if_addrs()
	interface_names = sorted(interfaces.keys())
	addresses = []
	for interface_name in interface_names:
		try:
			if interface_name[:3] in ["eth", "wla", "enp", "wlo", "wlp"]:
				ip_addr = next(
					address.address
						for address in interfaces[interface_name]
						if address.family == socket.AF_INET
				)
				addresses.append(ip_addr)
		except StopIteration:
			pass
	if len(addresses) == 0:
		raise NetworkError()

	return addresses


class MultiOrderedDict(OrderedDict):
	def __setitem__(self, key, value):
		if isinstance(value, list) and key in self and key in ["eth", "wlan", "emac", "wmac"]:
			self[key].extend(value)
		else:
			super(OrderedDict, self).__setitem__(key, value)


class Device:  # pylint: disable=too-many-instance-attributes
	"""A physical device"""
	config: ConfigParser = None
	config_all: ConfigParser = None
	devices: list = None
	current_ips: list = get_ips()
	# Config
	hostname: str
	wlan = str
	eth: str
	present: bool
	sync: str
	ssh: bool
	ssh_port: int
	mosh: bool
	emac: str
	wmac: str
	user: str
	relay: str
	relay_to: str
	ip_addr: str

	@staticmethod
	def get_devices(extra_config=None):
		"""Returns and stores the configured devices"""
		if not extra_config:
			extra_config = []

		general_devices_config: str = join(project_dir, 'devices.ini')
		local_devices_config: str = expanduser('~/sshtools/devices.ini')
		config_files = [general_devices_config, local_devices_config] + extra_config

		try:
			ssid = subprocess.check_output('iwgetid -r', shell=True).decode().strip("\n")
			if ssid == "WiFi-Home":
				config_files.append(join(project_dir, 'home.ini'))
			elif "Predikerinnenstraat 10" in ssid:
				config_files.append(join(project_dir, 'kot.ini'))
		except subprocess.CalledProcessError:
			logger.debug("WiFi not connected (or iwgetid can not be called)")

		ips = Device.current_ips
		ifaces = sorted(psutil.net_if_addrs().keys())
		# Give priority to my own routers (192.168.{23,24}.*) over the home routers (192.168.20.*)
		ip_id = ips[0][:10]
		if ip_id in ["192.168.23"] or 'tun0' in ifaces:
			# own kot network
			logger.info("Detected Tims Kot network.")
			config_files.append(join(project_dir, 'kot-tim.ini'))
		if ip_id in ["192.168.20"]:
			# Home network
			logger.info("Detected Home network.")
			config_files.append(join(project_dir, 'home.ini'))
		if ip_id in ["192.168.24"]:
			# Own home network
			logger.info("Detected Tims Home network.")
			config_files.append(join(project_dir, 'home-tim.ini'))

		Device.config_all = RawConfigParser(dict_type=MultiOrderedDict, strict=False)
		Device.config = ConfigParser()
		for config in [Device.config_all, Device.config]:
			config.read(config_files)
		Device.devices = Device.config.sections()

		return Device.devices

	def __init__(self, name, verbose=False):
		self.log = get_logger('ssh-tool.devices', verbose=verbose)
		self.name = name
		self.get_config(name)

	def get_config(self, name, relay=None):
		"""Loads and stores the device's config"""
		if relay:
			self.get_devices(extra_config=[expanduser(relay.relay_to)])
		elif not self.config:
			self.get_devices()

		try:
			self.hostname = self.config.get(name, 'hostname', fallback=self.name)
			self.wlan = self.config_all.get(name, 'wlan', fallback=None)
			self.eth = self.config_all.get(name, 'eth', fallback=None)
			self.present = self.wlan is not None or self.eth is not None
			self.sync = self.config.get(name, 'sync', fallback=True)
			self.ssh = self.config.getboolean(name, 'ssh', fallback=True)
			self.ssh_port = self.config.get(name, 'ssh_port', fallback=22)
			self.mosh = self.config.getboolean(name, 'mosh', fallback=False)
			self.emac = self.config.get(name, 'emac', fallback=None)
			self.wmac = self.config.get(name, 'wmac', fallback=None)
			self.user = self.config.get(name, 'user', fallback='tim')
			self.relay = self.config.get(name, 'relay', fallback=None)
			self.relay_to = self.config.get(name, 'relay_to', fallback=None)
			self.ip_addr = None
			if isinstance(self.sync, str):
				if self.sync == 'True':
					self.sync = True
				elif self.sync == 'False':
					self.sync = False
		except NoSectionError as error:
			raise DeviceNotFoundError(name) from error

	def get_ip(self) -> str:
		"""Returns the IP to used for the device"""
		if not self.eth and not self.wlan:
			raise DeviceNotPresentError(self.name)

		if self.hostname == os.uname().nodename:
			return self.hostname

		for ips in [
			list(reversed(ips))
			for ips in [self.eth, self.wlan, [self.hostname + ".local"]]
			if ips is not None
		]:
			alive_ips = check_ips(ips)
			if len(alive_ips) > 0:
				return alive_ips[0]

		raise NotReachableError(self.name)

	def get_relay(self):
		"""Return the relay device to be used when connecting to this device"""
		if self.relay:
			return Device(self.relay)
		return None

	def is_self(self) -> bool:
		"""Checks if the device is the currenct machine"""
		hostname_machine = os.uname().nodename
		return self.hostname == hostname_machine

	def is_local(self) -> bool:
		"""Checks if the device is present on the local LAN"""
		try:
			ip_addr: str = self.get_ip()
			return ip_addr is not None and ip_addr.startswith("192.168")
		except ErrorHandler:
			return False

	def __repr__(self):
		return '<Device({name})>'.format(name=self.hostname)


def check_ips(ip_addrs: List[str]) -> List[str]:
	"""Returns the IPs from a list that are reachable
	:param ip_addrs: A list of the IPs that need to be tested
	:returns: A list of reachable IPs"""

	ping_cmd = [
		"fping",
		"-q",  # don't report failed pings
		"-r 1",  # only try once
		"-a"  # only print alive ips
	]

	ping_out: str = bash.run(
		ping_cmd + ip_addrs,
		passable_exit_codes=[1, 2],
		capture_stdout=True
	)
	alive_ips: list = ping_out.split('\n')
	if '' in alive_ips:
		alive_ips.remove('')

	return alive_ips
