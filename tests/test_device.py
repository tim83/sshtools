import pytest

from sshtools import device, errors, ip


def test_creation():
    dev = device.Device("laptop")
    assert dev.name == "laptop"
    assert dev.hostname == "laptop-hostname"
    assert dev.mdns == "laptop-hostname.local"
    assert isinstance(dev.config.mosh, bool)
    assert isinstance(dev.config.ssh, bool)
    assert dev.config.sync in [True, False, "limited"]
    assert isinstance(dev.ip_address_list_all, ip.IPAddressList)
    assert isinstance(dev.reachable_ip_addresses, ip.IPAddressList)
    assert isinstance(dev.is_super, bool)
    assert isinstance(dev.is_main_device, bool)
    assert str(dev) == f"{dev}" == dev.hostname

    with pytest.raises(errors.DeviceNotFoundError):
        device.Device("doesnotexist")


def test_get_devices():
    dev_list = device.DeviceConfig.get_devices()
    assert isinstance(dev_list, list)
    assert all(isinstance(dev, device.Device) for dev in dev_list)


def test_name_or_hostname():
    assert device.DeviceConfig.get_name_from_hostname("laptop") == "laptop"
    assert device.DeviceConfig.get_name_from_hostname("laptop-hostname") == "laptop"
    assert device.Device("laptop") == device.Device("laptop-hostname")

    assert device.Device("laptop2") != device.Device("localhost")

    assert device.DeviceConfig.get_name_from_hostname("doesnotexist") == "doesnotexist"


def test_container_detection():
    assert device.DeviceConfig.get_name_from_hostname("desktop-container") == "desktop"
    assert device.Device("desktop-container") == device.Device("desktop")
    assert device.Device("desktop-container").is_container is True
    assert device.Device("desktop").is_container is False


def test_main_device():
    m_implied_dev = device.Device("laptop")
    nm_specified_dev = device.Device("testvm")
    nm_implied_dev = device.Device("desktop2")
    assert m_implied_dev.is_main_device is True
    assert nm_implied_dev.is_main_device is False
    assert nm_specified_dev.is_main_device is False


def test_singleton():
    assert device.Device("laptop") == device.Device("laptop")
    assert device.Device("laptop") == device.DeviceConfig.get_device("laptop")


def test_get_ip():
    for self_dev in [device.Device.get_self(), device.Device("localhost")]:
        print(f"Evaluating {self_dev}")
        assert self_dev.is_self is True
        assert self_dev.is_local is True
        assert self_dev.get_ip() == ip.IPAddress(self_dev.hostname)
        assert self_dev.ip_address == ip.IPAddress(self_dev.hostname)
        assert self_dev.get_ip(strict_ip=True) == ip.IPAddress("127.0.0.1")


def test_device_class():
    assert isinstance(device.DeviceConfig._get_config_all(), dict)
    devices = device.DeviceConfig.get_devices()
    assert isinstance(devices, list)
    assert all(isinstance(dev, device.Device) for dev in devices)


def test_super():
    assert device.Device("laptop").is_super is True
    assert device.Device("laptop2").is_super is False


def test_interface():
    dev = device.Device("laptop")
    assert len(dev.interfaces) == 3  # 1 of the device, 2 of the networks (vpns)
    iface = dev.interfaces[0]
    assert iface.name == "wlan0"
    assert isinstance(iface.mac, str)
    assert iface.device == dev


def test_network():
    dev = device.Device("laptop")
    ip_addr = next(
        filter(lambda ipa: ipa.network.name == "home", dev.ip_address_list_all), None
    )
    assert ip_addr is not None
    assert ip_addr.network.name == "home"
    assert ip_addr.network.interface == "wlan0"
    assert ip_addr.network.get_interface(dev).name == "wlan0"


def test_ip_construction():
    dev = device.Device("laptop")
    ips = [str(ipa) for ipa in dev.ip_address_list_all]
    # home
    assert "1.1.1.130" in ips
    # work
    assert "4.4.4.30" in ips
    # vpn
    assert "2.2.2.130" in ips
    # public
    assert "123.123.123" in ips
