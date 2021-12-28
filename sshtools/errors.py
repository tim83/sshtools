#! /usr/bin/python3
"""Errors to used by the modules"""

from __future__ import annotations  # python -3.9 compatibility

from timtools.log import get_logger

logger = get_logger(__name__)


class ErrorHandler(Exception):
    """General handler for errors"""

    logger = None

    def __init__(self, message):
        # if self.logger:
        #     self.logger.critical(message)
        # else:
        #     temp_log = get_logger(__name__)
        #     temp_log.critical(message)

        super().__init__(message)


class NotEmptyError(ErrorHandler):
    """Error to be raised when a mountpoint is not an empty directory"""

    def __init__(self, mountpoint):
        super().__init__(f"Mountpoint {mountpoint} is not empty.")


class NotReachableError(ErrorHandler):
    """Error to be raised when the device could not be reached"""

    def __init__(self, name):
        super().__init__(f"Device {name} could not be reached.")


class NetworkError(ErrorHandler):
    """Error to be raised when the device is not connected to the internet"""

    def __init__(self):
        super().__init__("You are not connected to the internet.")


class DeviceNotFoundError(ErrorHandler):
    """Error to be raised when the device is not configured"""

    def __init__(self, name):
        super().__init__(f"Device {name} was not found in the config.")


class DeviceNotPresentError(ErrorHandler):
    """Error to be raised when the device is not present"""

    def __init__(self, name):
        super().__init__(f"Device {name} is not present on this network.")


class ConfigError(ErrorHandler):
    """Error raised when there is problem with the config"""

    def __init__(self, name):
        super().__init__(f"Device {name} was not correctly configured for this action.")


class NetworkNotFound(ErrorHandler):
    """Error to be raised when the network is not configured"""

    def __init__(self, name):
        super().__init__(f"Network {name} was not found in the config.")
