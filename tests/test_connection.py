import pytest

from sshtools import connection, errors, ip


def test_creation():
    net = connection.Network("home")
    assert net.name == "home"
    assert net.is_vpn is False
    assert net.is_public is False

    pub_net = connection.Network("public")
    assert pub_net.name == "public"
    assert pub_net.is_vpn is False
    assert pub_net.is_public is True

    with pytest.raises(errors.NetworkNotFound):
        connection.Network("doesnotexist")


def test_singleton():
    assert connection.Network("home") == connection.Network("home")


def test_get_networks():
    assert isinstance(connection.Network.get_networks(), list)
    assert all(
        isinstance(net, connection.Network) for net in connection.Network.get_networks()
    )


def test_ip_ascosiation():
    home = connection.Network("home")
    assert home.has_ip_address(ip.IPAddress("192.168.20.132"))
    zt = connection.Network("zerotier")
    assert zt.has_ip_address(ip.IPAddress("192.168.193.150"))
    ztts = connection.Network("zerotier-techsupport")
    assert ztts.has_ip_address(ip.IPAddress("10.147.20.20"))
