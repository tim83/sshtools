from sshtools import device, interface


def test_eth_creation():
    dev = device.Device.get_self()

    for name, itype in [("eth0", "wired"), ("wlan3", "wifi")]:
        iface = interface.Interface(dev, name, mac="00:00:00:00:00")
        assert iface.device == dev
        assert iface.name == name
        assert iface.type == itype
        assert iface.mac == "00:00:00:00:00"


def test_interface_type():
    assert interface.Interface._determine_interface_type("wlp0s20f3") == "wifi"
    assert interface.Interface._determine_interface_type("wlan0") == "wifi"

    assert interface.Interface._determine_interface_type("enp0s20f3") == "wired"
    assert interface.Interface._determine_interface_type("eth0") == "wired"

    assert interface.Interface._determine_interface_type("randomword") == "unknown"
