#!  /usr/bin/python3
"""Module to wake up devices using wake on lan"""

from __future__ import annotations  # python -3.9 compatibility

import argparse

import timtools.log

import sshtools.device

logger = timtools.log.get_logger(__name__)


def wake(device: sshtools.device.Device):
    """Wake up a device"""
    for iface in device.interfaces:
        iface.wake()


def run():
    """Main executable for wake-up"""
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Welke computer is de referentie", nargs="?")
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    args = parser.parse_args()
    timtools.log.set_verbose(args.verbose)

    target = sshtools.device.Device(args.target)
    wake(target)


if __name__ == "__main__":
    run()
