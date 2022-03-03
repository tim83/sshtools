from __future__ import annotations  # python -3.9 compatibility

import tempfile
from pathlib import Path
from typing import Callable, Iterable

import timtools.locations
import timtools.multithreading

PROJECT_DIR = Path(__file__).parent

src_config_dir = PROJECT_DIR.parent / "config"
if not src_config_dir.is_dir():
    src_config_dir = (
        timtools.locations.get_user_home("tim") / "Programs/python/sshtools/config"
    )
user_config_dir = timtools.locations.get_user_config_dir() / "sshtools"
CONFIG_DIR: Path
if user_config_dir.is_dir():
    CONFIG_DIR = user_config_dir
else:
    CONFIG_DIR = src_config_dir

IP_CACHE_TIMEOUT: int = 5


def get_tmp_dir() -> Path:
    return Path(tempfile.mkdtemp())


def mt_filter(func: Callable, collection: Iterable, max_workers=20) -> list:
    """
    Filters a list based on a function, by using parallel processing
    :param func: The function that filters the list (must return a bool)
    :param collection: The list that needs to be filtered
    :param max_workers: The number of concurrent items that can be filtered
    :return: The filtered list
    """
    return timtools.multithreading.mt_filter(func, collection, max_workers=max_workers)
