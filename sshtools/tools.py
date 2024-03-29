"""Tools for use in the sshtools package"""
from __future__ import annotations  # python -3.9 compatibility

import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable

import tabulate
import timtools.bash
import timtools.locations
import timtools.multithreading

PROJECT_DIR = Path(__file__).parent

src_config_dir = PROJECT_DIR.parent / "config"
if not src_config_dir.is_dir():
    src_config_dir = (
        timtools.locations.get_user_home("tim") / "Programs/python/sshtools/config"
    )
user_config_dir = timtools.locations.get_user_config_dir() / "sshtools"
global_config_dir = Path("/etc/sshtools")
CONFIG_DIR: Path
if user_config_dir.is_dir():
    CONFIG_DIR = user_config_dir
elif global_config_dir.is_dir():
    CONFIG_DIR = global_config_dir
else:
    CONFIG_DIR = src_config_dir

IP_CACHE_TIMEOUT: int = 5
IP_PING_TIMEOUT: float = 1
IP_SSH_TIMEOUT: float = 4


def get_tmp_dir() -> Path:
    """
    Creates a temporary directory
    :return A Path for the temporary directory
    """
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


def mt_map(func: Callable, collection: Iterable, max_workers=20):
    """
    Filters a list based on a function, by using parallel processing
    :param func: The function that filters the list (must return a bool)
    :param collection: The list that needs to be filtered
    :param max_workers: The number of concurrent items that can be filtered
    """
    timtools.multithreading.mt_map(func, collection, max_workers=max_workers)


def str_to_bool(string: str, default: Any = False) -> bool:
    """
    Takes a string and converts it in a boolean (e.g. yes -> True)
    :param string: The string to convert
    :param default: The default value to return when there is no clear answer
    """
    string = string.lower()
    if string in ["true", "full", "yes", "ja", "y", "j"]:
        return True
    if string in ["false", "no", "nee", "n"]:
        return False

    return default


def create_table(
    add_row: Callable[[list, Any], Any],
    row_source: Iterable,
    sorting_key: Callable = None,
    **kwargs,
) -> tabulate.tabulate:
    """
    Prints a table containing the rows creating by running a 'add_row'
    on every item in 'row_source' in parallel.

    :param add_row:
        The function that takes an element from 'row_source' as input
        and returns a list of cells for that row
    :param row_source: The iterable that contains the base data for the rows
    :param sorting_key:
        The function used to sort the rows
        (will be an input for 'sorted(rows, key=sorting_key)'
    :param kwargs: Additional keyword arguments will be passed directly to tabulate

    :return: A 'tabulate' table object (can be printed simply with 'print(table)'
    """
    output: list[list] = []

    mt_map(lambda src: add_row(output, src), row_source)

    output_sorted = sorted(output, key=sorting_key)
    return tabulate.tabulate(output_sorted, **kwargs)


def execute_is_present(exec_name: str) -> bool:
    """
    Checks if a given executable is present on the system.
    The executable must be in $PATH, and the 'which' command must be present on the system.

    :param exec_name: str: Specify the name of the executable to check for
    :return: A boolean (true if the executable is present)
    """
    present_check: timtools.bash.CommandResult = timtools.bash.run(
        ["which", exec_name], passable_exit_codes=[0, 1]
    )
    return present_check.exit_code == 0
