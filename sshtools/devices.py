#! /usr/bin/python3
"""Classes for managing devices used by other files"""

import datetime as dt
import os
import socket
import subprocess
import threading
from collections import OrderedDict
from configparser import ConfigParser, NoSectionError, RawConfigParser
from os.path import dirname, expanduser, join
from typing import List, Optional, Union

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
	logger.debug(f"Networkinterfaces: {interface_names}")
	for interface_name in interface_names:
		try:
			if interface_name[:3] in ["eth", "wla", "enp", "wlo", "wlp", "eno"]:
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
	wlan: Union[str, list[str]]
	eth: Union[str, list[str]]
	present: bool
	sync: bool
	ssh: Union[str, bool]
	ssh_port: int
	mosh: bool
	emac: str
	wmac: str
	user: str
	relay: str
	relay_to: str
	ip_addr: Optional[str]
	mdns: Optional[str]

	unique_devices: dict[str, "Device"] = dict()

	@staticmethod
	def get_devices(extra_config=None):
		"""Returns and stores the configured devices"""
		if not extra_config:
			extra_config = []

		general_devices_config: str = join(project_dir, 'devices.ini')
		local_devices_config: str = expanduser('~/sshtools/devices.ini')
		config_files = [general_devices_config, local_devices_config] + extra_config

		try:
			ssid = subprocess.check_output(['/usr/sbin/iwgetid', '-r'], shell=True).decode().strip(
				"\n")
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
		if ip_id in ["192.168.193"] or "ztuga6wg3j" in ifaces:
			logger.info("Detected ZeroTier One VPN")
			config_files.append(join(project_dir, 'zerotier.ini'))

		Device.config_all = RawConfigParser(dict_type=MultiOrderedDict, strict=False)
		Device.config = ConfigParser(strict=False)
		for config in [Device.config_all, Device.config]:
			config.read(config_files)
		Device.devices = Device.config.sections()

		return Device.devices

	@staticmethod
	def get_device(name: str, verbose: bool = False):
		if name in Device.unique_devices.keys():
			return Device.unique_devices[name]

		return Device(name, verbose)

	def __init__(self, name: str, verbose: bool = False):
		self.logger = get_logger('ssh-tool.devices', verbose=verbose)
		if name not in Device.unique_devices.keys():
			Device.unique_devices[name] = self
		else:
			raise ValueError("A device object for this machine already exists")

		self.name = name
		self.get_config(name)
		self.last_ip_addr: Optional[str] = None
		self.last_ip_addr_update: Optional[dt.datetime] = None

	def get_config(self, name, relay=None):
		"""Loads and stores the device's config"""
		if relay:
			self.get_devices(extra_config=[expanduser(relay.relay_to)])
		elif not self.config:
			self.get_devices()

		try:
			self.hostname = self.config.get(name, 'hostname', fallback=None)
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
			if self.hostname is not None:
				self.mdns = self.hostname + ".local"
			else:
				self.mdns = None
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

		alive_ips = self.get_active_ips()
		if len(alive_ips) > 0:
			ip_addr = self.sort_ips(alive_ips)[0]
			logger.info(f"Found ip {ip_addr} for {self.name}")
			self.last_ip_addr = alive_ips[0]
			self.last_ip_addr_update = dt.datetime.now()
			return ip_addr

		raise NotReachableError(self.name)

	def sort_ips(self, ip_addrs: list[str]) -> list[str]:
		sorted_ips = {}
		# mDNS
		sorted_ips |= dict.fromkeys(filter(lambda ip: ip.endswith(".local"), ip_addrs))
		# Local IPs
		sorted_ips |= dict.fromkeys(filter(lambda ip: ip.startswith("192.168.2"), ip_addrs))
		# Zerotier IPs
		sorted_ips |= dict.fromkeys(filter(
			lambda ip: ip.startswith("192.168.193") or ip == self.hostname,
			ip_addrs
		))
		# Rest
		sorted_ips |= dict.fromkeys(ip_addrs)
		return list(sorted_ips.keys())

	def get_possible_ips(
			self,
			include_mdns: bool = True,
			include_hostname: bool = True,
			include_eth: bool = True,
			include_wlan: bool = True
	) -> list[str]:
		"""Returns all possible IPs that could be reached, within the given parameters"""

		possible_ips: list[str] = []

		def clean_ip_group(ip_group: Optional[list[str]]) -> list[str]:
			if ip_group is not None:
				return [ip for ip in ip_group if ip is not None and ip not in ['']]
			return []

		if include_eth:
			possible_ips += clean_ip_group(self.eth)
		if include_wlan:
			possible_ips += clean_ip_group(self.wlan)
		if include_mdns:
			possible_ips += clean_ip_group([self.mdns])
		if include_hostname:
			possible_ips += clean_ip_group([self.hostname])

		return possible_ips

	def get_active_ips(self) -> list[str]:
		"""Returns the list of all active ips"""
		possible_ips: list[str] = self.get_possible_ips()
		alive_ips: list[str] = check_ips(possible_ips)
		logger.info(f"Found {len(alive_ips)} alive IPs for device {self.name}: {alive_ips}")
		return alive_ips

	@property
	def ip_addr(self) -> str:
		if self.last_ip_addr is not None and self.last_ip_addr_update is not None:
			td_update: dt.timedelta = dt.datetime.now() - self.last_ip_addr_update
			if td_update < dt.timedelta(seconds=30):
				return self.last_ip_addr
		return self.get_ip()

	def get_relay(self):
		"""Return the relay device to be used when connecting to this device"""
		if self.relay:
			return Device.get_device(self.relay)
		return None

	def is_self(self) -> bool:
		"""Checks if the device is the currenct machine"""
		hostname_machine = os.uname().nodename
		return self.hostname == hostname_machine

	def is_local(self, include_vpn: bool = True) -> bool:
		"""
		Checks if the device is present on the local LAN
		:param include_vpn: Does a VPN (e.g. zerotier) count as part of the LAN?
		"""
		on_lan = lambda ip: ip.startswith("192.168") or ip.endswith(".local")
		vpn_used = lambda ip: ip.startswith("192.168.193")

		try:
			if self.ip_addr is not None:
				if on_lan(self.ip_addr):
					if include_vpn or not vpn_used(self.ip_addr):
						return True

				active_ips: list[str] = self.get_active_ips()
				local_ips = filter(on_lan, active_ips)
				for ip in local_ips:
					if not vpn_used(ip):
						return True
			return False
		except ErrorHandler:
			return False

	def is_present(self) -> bool:
		"""Checks if the device is reachable"""
		try:
			return self.ip_addr is not None
		except ErrorHandler:
			return False

	def __repr__(self):
		return '<Device({name})>'.format(name=self.hostname)


class IPThreads:
	num_threads = 3
	inputs: List[Optional[List[str]]] = [None] * num_threads
	output: List[Optional[List[str]]] = [None] * num_threads
	threads: List[Optional[threading.Thread]] = [None] * num_threads

	def start_all(self):
		for thread in self.threads:
			thread.start()

	@property
	def num_threads(self):
		return len(self.threads)


def check_ips_threading(ip_threads: IPThreads, index: int):
	"""Returns the IPs from a list that are reachable
	:param ip_threads: The object containing the threads, inputs and outputs for this job
	:param index: The index of this thread"""

	ip_addrs: List[str] = ip_threads.inputs[index]
	logger.debug(f"Trying {ip_addrs} [THREAD {index}]")

	for cmd_dir in ["/usr/bin", "/usr/sbin"]:
		cmd_location = os.path.join(cmd_dir, "fping")
		if os.path.exists(cmd_location):
			ping_cmd: list[str] = [cmd_location]
			break
	else:
		raise FileNotFoundError("Cannot find fping, is it installed?")

	ping_cmd += [
		"-q",  # don't report failed pings
		"-r 1",  # only try once
		"-a",  # only print alive ips
		"--timeout=250"  # limit timeout
	]

	ping_out: str = bash.get_output(
		ping_cmd + ip_addrs,
		passable_exit_codes=[1, 2],
		capture_stdout=True
	)
	alive_ips: list = ping_out.split('\n')
	if '' in alive_ips:
		alive_ips.remove('')

	ip_threads.output[index] = alive_ips


def check_ips(possible_ips: list[str]) -> list[str]:
	"""Returns the IPs from a list that are reachable
	:param possible_ips: The list of IPs to try
	"""

	logger.debug(f"Trying {possible_ips}")

	ping_cmd = [
		"/usr/sbin/fping",
		"-q",  # don't report failed pings
		"-r 1",  # only try once
		"-a"  # only print alive ips
	]

	ping_out: str = bash.get_output(
		ping_cmd + possible_ips,
		passable_exit_codes=[1, 2],
		capture_stdout=True
	)
	alive_ips: list = ping_out.split('\n')
	if '' in alive_ips:
		alive_ips.remove('')

	return alive_ips
