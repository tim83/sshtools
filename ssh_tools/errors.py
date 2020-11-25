#! /usr/bin/python3

from os.path import dirname

from timtools.log import get_logger

project_dir = dirname(__file__)
logger = get_logger(__name__)


class ErrorHandler(Exception):
	logger = None

	def __init__(self, message):
		if self.logger:
			self.logger.critical(message)
		else:
			temp_log = get_logger(__name__)
			temp_log.critical(message)

		super().__init__(message)


class ConnectionError(ErrorHandler):
	def __init__(self, name):
		super().__init__(f'Device {name} could not be reached.')


class NetworkError(ErrorHandler):
	def __init__(self):
		super().__init__(f'You are not connected to the internet.')


class DeviceNotFoundError(ErrorHandler):
	def __init__(self, name):
		super().__init__(f'Device {name} not found.')


class DeviceNotPresentError(ErrorHandler):
	def __init__(self, name):
		super().__init__(f'Device {name} is not present on this network.')


class ConfigError(ErrorHandler):
	def __init__(self, name):
		super().__init__(f'Device {name} was not correctly configured for this action.')
