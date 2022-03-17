"""Package for connecting to and interacting with devices over the network"""
from __future__ import annotations

import platform

import timtools.log

logger = timtools.log.get_logger(__name__)
logger.debug("Python version: %s", platform.python_version())
