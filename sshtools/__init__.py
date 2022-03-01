#! /usr/bin/python3
from __future__ import annotations

import platform

import timtools.log

logger = timtools.log.get_logger(__name__)
logger.debug(f"Python version: {platform.python_version()}")
