import pytest

from sshtools import device, errors, ip


def test_creation():
    dev = device.Device("laptop")
    assert dev.name == "laptop"
    assert dev.hostname == "laptop-tim"
    assert dev.mdns == "laptop-tim.local"
    assert isinstance(dev.config.mosh, bool)
    assert isinstance(dev.config.ssh, bool)
    assert dev.config.sync in [True, False, "limited"]
    assert isinstance(dev.ip_address_list_all, ip.IPAddressList)
    assert isinstance(dev.reachable_ip_addresses, ip.IPAddressList)
    assert isinstance(dev.is_super, bool)
    assert isinstance(dev.is_main_device, bool)

    with pytest.raises(errors.DeviceNotFoundError):
        device.Device("doesnotexist")


def test_main_device():
    m_implied_dev = device.Device("laptop")
    nm_specified_dev = device.Device("testvm")
    nm_implied_dev = device.Device("desktop-ben")
    assert m_implied_dev.is_main_device is True
    assert nm_implied_dev.is_main_device is False
    assert nm_specified_dev.is_main_device is False


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
    assert isinstance(device.Device._get_config_all(), dict)
    devices = device.Device.get_devices()
    assert isinstance(devices, list)
    assert all(isinstance(dev, device.Device) for dev in devices)


def test_super():
    assert device.Device("laptop").is_super is True
    assert device.Device("probook").is_super is False
