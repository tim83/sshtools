#! /usr/bin/python3
"""Information for packaging the module"""

from setuptools import setup

# from distutils.core import setup

setup(
	name='sshtools',
	version='2.04.1',
	packages=['sshtools'],
	url='',
	license='',
	author='Tim Mees',
	author_email='tim@mees.vip',
	description='PERSONAL USE ONLY: set of tools for connecting with SSH to my machines',
	install_requires=[
		'datetime',
		'argparse',
		'configparser',
		'psutil',
		'timtools',
		'fping',
	],
	scripts=[
		"bin/getip",
		"bin/sshin",
		"bin/ssync",
		"bin/wake-up",
		"bin/smount",
	],
	include_package_data=True,
	data_files=[(
		'',
		[f'sshtools/{filename}.ini' for filename in ["devices", "kot", "kot-tim", "home", "home-tim"]] +
		[f'sshtools/{filename}.txt' for filename in ["exclude", "include", "limited"]]
	)]
)
