import sshtools.connection
import sshtools.device
import sshtools.pathfinder


def test_get_device_networks():
    pf = sshtools.pathfinder.PathFinder
    dev_networks = pf.get_device_networks(sshtools.device.Device("serverpi"))
    assert isinstance(dev_networks, list)
    assert any(
        isinstance(network, sshtools.connection.Network) for network in dev_networks
    )
    assert sorted([network.name for network in dev_networks]) == sorted(
        ["kot-tim", "zerotier"]
    )
