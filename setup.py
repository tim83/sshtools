#! /usr/bin/python3
"""Information for packaging the module"""

from setuptools import setup

# from distutils.core import setup

setup(
    name="sshtools",
    version="4.0.1",
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
