import datetime as dt
import socket

import pytest
from timtools import log

import sshtools.connection
import sshtools.ip
import sshtools.tools
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


def test_singleton():
    """Tests whether multiple object with the same IP are singletons"""
    assert ip.IPAddress("localhost") == ip.IPAddress("localhost")


def test_create_hostname():
    """Tests the creation of an IPAddress model with a hostname"""
    for ip_str in ["localhost", "laptop-hostname.local"]:
        ipv6 = ip.IPAddress(ip_str)
        assert ipv6.ip_address == ip_str
        assert ipv6.version == 0


def test_vpn():
    """Tests whether an IP is correctly identified as a VPN"""
    assert sshtools.ip.IPAddress("2.2.2.20").is_vpn is True
    assert sshtools.ip.IPAddress("3.3.3.130").is_vpn is True

    assert sshtools.ip.IPAddress("192.168.20.140").is_vpn is False
    assert sshtools.ip.IPAddress("8.8.8.8").is_vpn is False
    assert sshtools.ip.IPAddress("127.0.0.1").is_vpn is False


def test_local():
    """Tests the check whether the IP is local"""
    test_ips = [
        ("localhost", True, False, True),
        (socket.gethostname(), True, False, True),
        ("127.0.0.1", True, False, True),
        ("::1", True, False, True),
        ("2.2.2.116", True, True, False),
        ("143.169.210.13", False, False, False),
        ("ff80::94b6:ff97:1c37:3f66", False, False, False),
        ("arandomcomputer.local", True, False, False),
        ("3.3.3.130", False, False, False),
    ]
    for ip_str, is_local, is_vpn, is_loopback in test_ips:
        ip_address = ip.IPAddress(ip_str)
        assert ip_address.is_local(include_vpn=True) == is_local
        assert ip_address.is_local(include_vpn=False) == (is_local and not is_vpn)
        assert ip_address.is_loopback == is_loopback


def test_alive():
    """Tests the check whether the IP is alive"""
    assert ip.IPAddress("localhost").is_alive
    assert not ip.IPAddress("doesnotexists").is_alive


def test_str_conversion():
    """Tests that convert an instance to a string returns the ip address"""
    assert str(ip.IPAddress("localhost")) == "localhost"
    assert str(ip.IPAddress("1.1.1.2")) == "1.1.1.2"


def test_list_creation():
    """Tests the creation of ip lists"""
    assert ip.IPAddressList()._ip_addresses == []
    example_ip = ip.IPAddress("127.0.0.1")
    assert ip.IPAddressList(ip_addresses=[example_ip])._ip_addresses == [example_ip]


def test_list_add():
    init_ip = ip.IPAddress("localhost")
    ip_list = ip.IPAddressList([init_ip])
    example_ip = ip.IPAddress("127.0.0.1")
    ip_list.add(example_ip)
    assert ip_list._ip_addresses == [init_ip, example_ip]


def test_list_add_list():
    init_ip = ip.IPAddress("localhost")
    ip_list = ip.IPAddressList([init_ip])
    example_ip_list = [ip.IPAddress("127.0.0.1"), ip.IPAddress("::1")]
    ip_list.add_list(example_ip_list)
    assert ip_list._ip_addresses == [init_ip] + example_ip_list

    ip_list = ip.IPAddressList([init_ip])
    ip_list.add_list(ip.IPAddressList(example_ip_list))
    assert ip_list._ip_addresses == [init_ip] + example_ip_list


def test_sort_ips():
    ip_list = ip.IPAddressList(
        [ip.IPAddress("localhost"), ip.IPAddress("127.0.0.1"), ip.IPAddress("1.1.1.1")]
    )
    assert ip_list._is_sorted is False
    ip_list.sort_ips()
    assert ip_list._is_sorted is True


def test_list_alive():
    alive_ips = [ip.IPAddress("127.0.0.1"), ip.IPAddress("localhost")]
    ip_list = ip.IPAddressList(alive_ips + [ip.IPAddress("doesnotexists.local")])

    start_time = dt.datetime.now()
    alive_list = ip_list.get_alive_addresses()
    end_time = dt.datetime.now()

    assert alive_list._ip_addresses == sorted(alive_ips, key=lambda i: str(i))

    process_time = end_time - start_time
    assert (
        process_time.total_seconds()
        < (ip_list.length * sshtools.tools.IP_PING_TIMEOUT) + 1
    )


def test_list_length():
    ip_list = ip.IPAddressList(
        [
            ip.IPAddress("127.0.0.1"),
            ip.IPAddress("localhost"),
            ip.IPAddress("doesnotexists.local"),
        ]
    )
    assert ip_list.length == 3


def test_list_to_list():
    ips = [
        ip.IPAddress("127.0.0.1"),
        ip.IPAddress("localhost"),
        ip.IPAddress("doesnotexists.local"),
    ]
    ip_list = ip.IPAddressList(ips)
    extra_ip = ip.IPAddress("example.com")
    ip_list.add(extra_ip)
    assert ip_list.list == ips + [extra_ip]
