from __future__ import annotations  # python -3.9 compatibility

import concurrent.futures
from pathlib import Path
from typing import Callable, Iterable

PROJECT_DIR = Path(__file__).parent

src_config_dir = PROJECT_DIR.parent / "config"
user_config_dir = Path.home() / ".config/sshtools"
CONFIG_DIR: Path
if user_config_dir.is_dir():
    CONFIG_DIR = user_config_dir
else:
    CONFIG_DIR = src_config_dir


def mt_filter(func: Callable, collection: Iterable, max_workers=20) -> list:
    filtered_collection = []

    def filter_item(item):
        if func(item) is True:
            filtered_collection.append(item)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(filter_item, collection)

    return filtered_collection
