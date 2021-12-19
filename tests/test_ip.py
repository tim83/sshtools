import os

import pytest
from timtools import log

from sshtools import ip

log.set_verbose(True)


def test_create_ipv4():
    """Tests the creation of an IPAddress model with an IPv4 address"""
    ipv4 = ip.IPAddress("143.169.210.13")
    assert ipv4.ip_address == "143.169.210.13"
    assert ipv4.version == 4

    with pytest.raises(ValueError):
        ip.IPAddress("Lorem ipsum")


def test_create_ipv6():
    """Tests the creation of an IPAddress model with an IPv6 address"""
    for ip_str in ["fe80::94b6:ff97:1c37:3f66", "::1"]:
        ipv6 = ip.IPAddress(ip_str)
        assert ipv6.ip_address == ip_str
        assert ipv6.version == 6

    with pytest.raises(ValueError):
        ip.IPAddress("fe80::94b6:ff97:1c37:3f66123")
    with pytest.raises(ValueError):
        ip.IPAddress("fe80::94b6:ff97:1c37::3f66")


def test_create_hostname():
    """Tests the creation of an IPAddress model with a hostname"""
    for ip_str in ["localhost", "laptop-tim.local", "mees.vip"]:
        ipv6 = ip.IPAddress(ip_str)
        assert ipv6.ip_address == ip_str
        assert ipv6.version == 0


def test_local():
    """Tests the check whether the IP is local"""
    test_ips = [
        ("localhost", True, False),
        (os.uname().nodename, True, False),
        ("127.0.0.1", True, False),
        ("::1", True, False),
        ("192.168.193.116", True, True),
        ("143.169.210.13", False, False),
        ("ff80::94b6:ff97:1c37:3f66", False, False),
    ]
    for ip_str, is_local, is_vpn in test_ips:
        ip_addr = ip.IPAddress(ip_str)
        assert ip_addr.is_local(include_vpn=True) == is_local
        assert ip_addr.is_local(include_vpn=False) == (is_local and not is_vpn)


def test_alive():
    """Tests the check whether the IP is alive"""
    assert ip.IPAddress("localhost").is_alive()
    assert not ip.IPAddress("doesnotexists").is_alive()
