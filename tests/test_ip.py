import datetime as dt
import socket

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


def test_singleton():
    """Tests wheter mutliple object with the same IP are singletons"""
    assert ip.IPAddress("localhost") == ip.IPAddress("localhost")


def test_create_hostname():
    """Tests the creation of an IPAddress model with a hostname"""
    for ip_str in ["localhost", "laptop-tim.local", "mees.vip"]:
        ipv6 = ip.IPAddress(ip_str)
        assert ipv6.ip_address == ip_str
        assert ipv6.version == 0


def test_local():
    """Tests the check whether the IP is local"""
    test_ips = [
        ("localhost", True, False, True),
        (socket.gethostname(), True, False, True),
        ("127.0.0.1", True, False, True),
        ("::1", True, False, True),
        ("192.168.193.116", True, True, False),
        ("143.169.210.13", False, False, False),
        ("ff80::94b6:ff97:1c37:3f66", False, False, False),
        ("arandomcomputer.local", True, False, False),
    ]
    for ip_str, is_local, is_vpn, is_loopback in test_ips:
        ip_addr = ip.IPAddress(ip_str)
        assert ip_addr.is_local(include_vpn=True) == is_local
        assert ip_addr.is_local(include_vpn=False) == (is_local and not is_vpn)
        assert ip_addr.is_loopback() == is_loopback


def test_alive():
    """Tests the check whether the IP is alive"""
    assert ip.IPAddress("localhost").is_alive()
    assert not ip.IPAddress("doesnotexists").is_alive()


def test_str_conversion():
    """Tests that convert an instance to a string returns the ip address"""
    assert str(ip.IPAddress("localhost")) == "localhost"
    assert str(ip.IPAddress("192.168.23.2")) == "192.168.23.2"


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
    loc_ip = ip.IPAddress("localhost")
    loop_ip = ip.IPAddress("127.0.0.1")
    mdns_ip = ip.IPAddress("hostname.local")
    lan_ip = ip.IPAddress("192.168.20.15")
    ztts_ip = ip.IPAddress("10.147.20.130")
    zt_ip = ip.IPAddress("192.168.193.150")
    pub_ip = ip.IPAddress("32.102.39.10")
    dns_ip = ip.IPAddress("mees.vip")
    ip_list = ip.IPAddressList(
        [dns_ip, mdns_ip, lan_ip, loc_ip, ztts_ip, zt_ip, pub_ip, loop_ip]
    )
    ip_list.sort_ips()
    assert ip_list._ip_addresses == [
        loop_ip,
        loc_ip,
        mdns_ip,
        lan_ip,
        zt_ip,
        ztts_ip,
        pub_ip,
        dns_ip,
    ]
    assert ip_list.get_first() == loop_ip


def test_list_alive():
    start_time = dt.datetime.now()
    alive_ips = [ip.IPAddress("127.0.0.1"), ip.IPAddress("localhost")]
    ip_list = ip.IPAddressList(alive_ips + [ip.IPAddress("doesnotexists.local")])
    alive_list = ip_list.get_alive_addresses()
    end_time = dt.datetime.now()
    alive_list.sort_ips()
    assert alive_list._ip_addresses == alive_ips
    process_time = end_time - start_time
    assert process_time.total_seconds() < 5


def test_list_length():
    ip_list = ip.IPAddressList(
        [
            ip.IPAddress("127.0.0.1"),
            ip.IPAddress("localhost"),
            ip.IPAddress("doesnotexists.local"),
        ]
    )
    assert ip_list.length() == 3


def test_list_to_list():
    ips = [
        ip.IPAddress("127.0.0.1"),
        ip.IPAddress("localhost"),
        ip.IPAddress("doesnotexists.local"),
    ]
    ip_list = ip.IPAddressList(ips)
    extra_ip = ip.IPAddress("example.com")
    ip_list.add(extra_ip)
    assert ip_list.to_list() == ips + [extra_ip]
