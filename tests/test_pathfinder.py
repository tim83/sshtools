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


def test_possible_relays():
    pf = sshtools.pathfinder.PathFinder(
        sshtools.device.Device("thinkcentre"),
        source=sshtools.device.Device("coolermaster"),
    )
    for dev_name in ("serverpi", "oracle", "probook"):
        possible_relay = pf.device_is_a_possible_relay(sshtools.device.Device(dev_name))
        assert isinstance(possible_relay, bool)
        assert possible_relay is True


def test_path():
    dev_path = [sshtools.device.Device("oracle"), sshtools.device.Device("thinkcentre")]
    path = sshtools.pathfinder.Path(dev_path)
    assert path.device_route == dev_path


def test_local_path():
    start_dev = sshtools.device.Device("serverpi")
    end_dev = sshtools.device.Device("thinkcentre")
    pf = sshtools.pathfinder.PathFinder(end_dev, source=start_dev)

    pp = pf.possible_paths
    assert isinstance(pp, list)
    assert any(isinstance(path, sshtools.pathfinder.Path) for path in pp)

    print(pp)
    path = pp[0]
    assert isinstance(path, sshtools.pathfinder.Path)
    assert len(path.device_route) == 1
    assert start_dev not in path.device_route
    assert path.device_route[-1] == end_dev


def test_sort_paths():
    pf = sshtools.pathfinder.PathFinder
    p1 = sshtools.pathfinder.Path(
        [sshtools.device.Device("serverpi"), sshtools.device.Device("thinkcentre")]
    )
    p2 = sshtools.pathfinder.Path(
        [
            sshtools.device.Device("serverpi"),
            sshtools.device.Device("oracle"),
            sshtools.device.Device("thinkcentre"),
        ]
    )
    assert pf.sort_paths([p2, p1]) == [p1, p2]


def test_pathfinder():
    target = sshtools.device.Device("thinkcentre")
    source = sshtools.device.Device("serverpi")
    pf1 = sshtools.pathfinder.PathFinder(target)
    assert pf1.target == target
    assert pf1.source == sshtools.device.Device.get_self()

    pf2 = sshtools.pathfinder.PathFinder(target, source=source)
    assert pf2.target == target
    assert pf2.source == source


def test_find_path():
    target = sshtools.device.Device.get_self()
    pf = sshtools.pathfinder.PathFinder(target)
    path = pf.find_path()
    assert path == pf.path
    assert isinstance(path, sshtools.pathfinder.Path) or path is None
