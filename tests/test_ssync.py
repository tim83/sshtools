import sshtools.device
import sshtools.ssync


def test_relevant_devices():
    master, slaves = sshtools.ssync.get_relevant_devices(None, None, None)
    assert master == sshtools.device.Device.get_self()
    assert isinstance(slaves, list)
    assert len(slaves) > 2
    assert all(isinstance(slave, sshtools.device.Device) for slave in slaves)
    assert master not in slaves

    master, slaves = sshtools.ssync.get_relevant_devices("desktop", None, None)
    assert master == sshtools.device.Device("desktop")
    assert len(slaves) > 2
    assert master not in slaves

    master, slaves = sshtools.ssync.get_relevant_devices(None, "laptop", "desktop")
    assert master == sshtools.device.Device("laptop")
    assert slaves == [sshtools.device.Device("desktop")]

    master, slaves = sshtools.ssync.get_relevant_devices(None, None, "pi")
    assert master == sshtools.device.Device.get_self()
    assert slaves == [sshtools.device.Device("pi")]

    master, slaves = sshtools.ssync.get_relevant_devices(None, "desktop", None)
    assert master == sshtools.device.Device("desktop")
    assert slaves == [sshtools.device.Device.get_self()]
