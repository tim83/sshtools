"""Errors to used by the modules"""

from __future__ import annotations  # python -3.9 compatibility

import timtools.log

logger = timtools.log.get_logger("sshtools.errors")


class ErrorHandler(Exception):
    """General handler for errors"""

    logger = None


class NotEmptyError(ErrorHandler):
    """Error to be raised when a mount point is not an empty directory"""

    def __init__(self, mount_point):
        super().__init__(f"Mount point {mount_point} is not empty.")


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
