import pytest

import sshtools.device
import sshtools.interface
from sshtools import connection, errors, ip


def test_creation():
    net = connection.Network("home")
    assert net.name == "home"
    assert net.is_vpn is False
    assert net.is_public is False
    assert net.priority == 80

    net = connection.Network("vpn")
    assert net.name == "vpn"
    assert net.is_vpn is True
    assert net.is_public is False
    assert net.priority == 60

    net = connection.Network("family")
    assert net.name == "family"
    assert net.is_vpn is True
    assert net.is_public is True
    assert net.priority == 20

    pub_net = connection.Network("public")
    assert pub_net.name == "public"
    assert pub_net.is_vpn is False
    assert pub_net.is_public is True
    assert pub_net.priority == 50

    with pytest.raises(errors.NetworkNotFound):
        connection.Network("doesnotexist")


def test_singleton():
    assert connection.Network("home") == connection.Network("home")


def test_get_networks():
    assert isinstance(connection.Network.get_networks(), list)
    assert all(
        isinstance(net, connection.Network) for net in connection.Network.get_networks()
    )


def test_get_interface():
    network = connection.Network("vpn")
    device = sshtools.device.Device("laptop")

    interface = network.get_interface(device)
    assert isinstance(interface, sshtools.interface.Interface)
    assert interface.name == network.interface

    assert network.get_interface(sshtools.device.Device("testvm")) is None


def test_get_construct_ip():
    device = sshtools.device.Device("laptop")

    for network_name, ip_str in [
        ("vpn", "2.2.2.130"),
        ("work", "4.4.4.30"),
    ]:
        network = connection.Network(network_name)
        ip_addr = network.construct_ip(device)
        assert isinstance(ip_addr, ip.IPAddress)
        assert str(ip_addr) == ip_str


def test_ip_association():
    home = connection.Network("home")
    assert home.has_ip_address(ip.IPAddress("1.1.1.132"))
    zt = connection.Network("vpn")
    assert zt.has_ip_address(ip.IPAddress("2.2.2.150"))
    ztts = connection.Network("family")
    assert ztts.has_ip_address(ip.IPAddress("3.3.3.20"))
