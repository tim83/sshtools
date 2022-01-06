import pytest

from sshtools import device, errors, ip


def test_creation():
    dev = device.Device("laptop")
    assert dev.name == "laptop"
    assert dev.hostname == "laptop-tim"
    assert type(dev.config.mosh) == bool
    assert type(dev.config.ssh) == bool
    assert dev.config.sync in [True, False, "limited"]
    assert type(dev.ip_address_list_all) == ip.IPAddressList
    assert type(dev.reachable_ip_addresses) == ip.IPAddressList

    with pytest.raises(errors.DeviceNotFoundError):
        device.Device("doesnotexist")


def test_singleton():
    assert device.Device("laptop") == device.Device("laptop")
    assert device.Device("laptop") == device.Device.get_device("laptop")


def test_get_ip():
    for self_dev in [device.Device.get_self(), device.Device("localhost")]:
        assert self_dev.is_self() is True
        assert self_dev.is_local() is True
        assert self_dev.get_ip() == ip.IPAddress("localhost")
        assert self_dev.get_ip(strict_ip=True) == ip.IPAddress("127.0.0.1")


def test_device_class():
    assert type(device.Device._get_config_all()) == dict
    devices = device.Device.get_devices()
    assert type(devices) == list
    assert all(type(dev) == device.Device for dev in devices)


def test_super():
    assert device.Device("laptop").is_super is True
    assert device.Device("probook").is_super is False
