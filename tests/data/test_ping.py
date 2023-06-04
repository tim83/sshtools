import collections
import datetime

import pytest

from sshtools.data import ping

CompletedProcess: collections.namedtuple = collections.namedtuple(
    "CompletedProcess", ["returncode", "stdout", "stderr"]
)


def test_ping_creation():
    p = ping.Ping("target_ip")
    assert isinstance(p, ping.Ping)
    assert p.target == "target_ip"


def test__process_ping_result_alive():
    stdout = """
    PING google.com (172.253.120.100) 56(84) bytes of data.

    --- google.com ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 23.504/23.504/23.504/0.000 ms"""

    ping_result = CompletedProcess(returncode=0, stderr="", stdout=stdout)
    alive, latency = ping.Ping._process_ping_result(ping_result)
    assert alive is True
    assert latency == datetime.timedelta(milliseconds=23.504)


def test__process_ping_result_unalive():
    ping_result = CompletedProcess(
        returncode=2,
        stderr="ping: doesnotexist.be: Naam of dienst is niet bekend",
        stdout="",
    )
    alive, latency = ping.Ping._process_ping_result(ping_result)
    assert alive is False
    assert latency == datetime.timedelta.max
    assert latency > datetime.timedelta(hours=1)


def test__process_ping_result_failure():
    ping_result = CompletedProcess(
        returncode=1, stderr="ping: usage error: Doeladres vereist", stdout=""
    )

    with pytest.raises(ValueError):
        ping.Ping._process_ping_result(ping_result)
