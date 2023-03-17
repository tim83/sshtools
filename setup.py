"""Information for packaging the module"""

from pathlib import Path

import toml
from setuptools import setup

pyproject_path = Path(__file__).parent / "pyproject.toml"
with open(pyproject_path, "r", encoding="utf-8") as fobj:
    toml_str = fobj.read()
    parsed_toml = toml.loads(toml_str)

setup(
    name="sshtools",
    version=parsed_toml["tool"]["poetry"]["version"],
    packages=["sshtools"],
    url="https://github.com/tim83/sshtools",
    license="",
    author="Tim Mees",
    author_email="tim@mees.vip",
    description="PERSONAL USE ONLY: set of tools for connecting with SSH to my machines",
    install_requires=[
        "argparse",
        "configparser",
        "psutil",
        "timtools",
        "pathlib",
        "tabulate",
    ],
    scripts=[
        "bin/getip",
        "bin/sshin",
        "bin/ssync",
        "bin/wake-up",
        "bin/smount",
    ],
)
