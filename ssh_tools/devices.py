#! /usr/bin/python3

import os
import socket
import subprocess
from configparser import ConfigParser, NoSectionError
from os.path import join, dirname, expanduser

import psutil

from timtools.log import get_logger
from errors import NetworkError, DeviceNotFoundError, DeviceNotPresentError, ErrorHandler

project_dir = dirname(__file__)
logger = get_logger("ssh-tools.devices")


def get_ips():
	interfaces = psutil.net_if_addrs()
	interface_names = sorted(interfaces.keys())
	addresses = []
	for interface_name in interface_names:
		try:
			if interface_name[:3] in ["eth", "wla", "enp", "wlo", "wlp"]:
				ip = next(address.address for address in interfaces[interface_name] if address.family == socket.AF_INET)
				addresses.append(ip)
		except StopIteration:
			pass
	if len(addresses) == 0:
		raise NetworkError()
	else:
		return addresses


class Device(object):
	config: ConfigParser = None
	devices: list = None
	current_ips: list = get_ips()

	@staticmethod
	def get_devices(extra_config=None):
		if not extra_config:
			extra_config = []

		config_files = [join(project_dir, 'devices.ini'), expanduser('~/ssh_tools/devices.ini')] + extra_config

		try:
			ssid = subprocess.check_output('iwgetid -r', shell=True).decode().strip("\n")
			if ssid == "WiFi-Home":
				config_files.append(join(project_dir, 'home.ini'))
			elif "Predikerinnenstraat 10" in ssid:
				config_files.append(join(project_dir, 'kot.ini'))
		except subprocess.CalledProcessError:
			logger.debug("WiFi not connected (or iwgetid can not be called)")

		ips = Device.current_ips  # gives priority to my own routers (192.168.{23,24}.*) over the home routers (192.168.20.*)
		ip_id = ips[0][:10]
		if ip_id in ["192.168.20"]:
			# Home network
			logger.info("Detected Home network.")
			config_files.append(join(project_dir, 'home.ini'))
		elif ip_id in ["192.168.24"]:
			# Own home network
			logger.info("Detected Tims Home network.")
			config_files.append(join(project_dir, 'home-tim.ini'))
		elif ip_id in ["192.168.23"]:
			# own kot network
			logger.info("Detected Tims Kot network.")
			config_files.append(join(project_dir, 'kot-tim.ini'))

		Device.config = ConfigParser()
		Device.config.read(config_files)
		Device.devices = Device.config.sections()

		return Device.devices

	def __init__(self, name, verbose=False):
		self.log = get_logger('ssh-tool.devices', verbose=verbose)
		self.name = name
		self.get_config(name)

	def get_config(self, name, relay=None):
		if relay:
			self.get_devices(extra_config=[expanduser(relay.relay_to)])
		elif not self.config:
			self.get_devices()

		try:
			self.hostname = self.config.get(name, 'hostname', fallback=self.name)
			self.wlan = self.config.get(name, 'wlan', fallback=None)
			self.eth = self.config.get(name, 'eth', fallback=None)
			self.present = self.wlan or self.eth
			self.sync = self.config.get(name, 'sync', fallback=True)
			self.ssh = self.config.getboolean(name, 'ssh', fallback=True)
			self.ssh_port = self.config.get(name, 'ssh_port', fallback=22)
			self.mosh = self.config.getboolean(name, 'mosh', fallback=False)
			self.ssh_port = self.config.get(name, 'ssh_port', fallback='22')
			self.emac = self.config.get(name, 'emac', fallback=None)
			self.wmac = self.config.get(name, 'wmac', fallback=None)
			self.user = self.config.get(name, 'user', fallback='tim')
			self.relay = self.config.get(name, 'relay', fallback=None)
			self.relay_to = self.config.get(name, 'relay_to', fallback=None)
			self.ip = None
			if type(self.sync) == str:
				if self.sync == 'True':
					self.sync = True
				elif self.sync == 'False':
					self.sync = False
		except NoSectionError:
			raise DeviceNotFoundError(name)

	def get_ip(self):
		for ip in self.eth, self.wlan:
			if ip:
				response = os.system(f'ping -c 1 {ip} > /dev/null')
				if response == 0:  # or self.name == "serverpi":
					self.ip = ip
					return ip
		else:
			if not self.eth and not self.wlan:
				raise DeviceNotPresentError(self.name)
			else:
				# Check if one of the interfaces is connected to a different network that the one just used
				selected_network_id = Device.current_ips[0][10:]  # Extract the "192.168.XX" part of the IP
				alternative_ips = [ip for ip in Device.current_ips if selected_network_id not in ip]  # Filter out all ips in the same subnet
				if len(alternative_ips) >= 1:
					logger.info(f"Could not find {self.name} in the selected network")
					Device.current_ips = alternative_ips
					self.get_config(self.name)
					return self.get_ip()
				else:
					raise ConnectionError(self.name)

	def get_relay(self):
		if self.relay:
			return Device(self.relay)
		else:
			return None

	def is_self(self):
		hostname_machine = os.uname().nodename
		return self.hostname == hostname_machine

	def is_local(self):
		try:
			if not self.ip:
				self.get_ip()

			return self.ip.startswith("192.168")
		except ErrorHandler:
			return False

	def __repr__(self):
		return '<Device({name})>'.format(name=self.hostname)
