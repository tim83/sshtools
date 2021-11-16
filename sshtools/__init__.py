#! /usr/bin/python3

import platform

import timtools

logger = timtools.log.get_logger(__name__)
logger.debug(f"Python version: {platform.python_version()}")
