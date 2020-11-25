#! /usr/bin/python3

from setuptools import setup

# from distutils.core import setup

setup(
	name='ssh_tools',
	version='1.91',
	packages=['ssh_tools'],
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
	],
	scripts=[
		"bin/getip",
		"bin/sshin",
		"bin/ssync",
		"bin/wake-up",
		"bin/smount",
	],
	include_package_data=True,
	data_files=[
		('',
		[f'ssh_tools/{filename}.ini' for filename in ["devices", "kot", "kot-tim", "home", "home-tim"]] +
		[f'ssh_tools/{filename}.txt' for filename in ["exclude", "include", "limited"]]
		),
	]
)
