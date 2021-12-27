import pytest

from sshtools import connection, errors


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
    assert type(connection.Network.get_networks()) == list
    assert all(
        type(net) == connection.Network for net in connection.Network.get_networks()
    )
