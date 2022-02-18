import timtools.log

import sshtools.connection
import sshtools.device
import sshtools.pathfinder

timtools.log.set_verbose(True)


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


def test_is_same_network():
    pf = sshtools.pathfinder.PathFinder
    in_same_network = pf.in_same_network(
        sshtools.device.Device("serverpi"), sshtools.device.Device("thinkcentre")
    )
    assert isinstance(in_same_network, bool)
    assert in_same_network is True


def test_local_path():
    pf = sshtools.pathfinder.PathFinder(
        sshtools.device.Device("serverpi"), sshtools.device.Device("thinkcentre")
    )
    pf.find_path()
    assert isinstance(pf.path, list)
    assert any(isinstance(node, sshtools.device.Device) for node in pf.path)
    assert len(pf.path) == 1
