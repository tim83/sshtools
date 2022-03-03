import tempfile
from pathlib import Path

import sshtools.device
import sshtools.ssync


def test_relevant_devices():
    master, slaves = sshtools.ssync.get_relevant_devices(None, None, None)
    assert master == sshtools.device.Device.get_self()
    assert isinstance(slaves, list)
    assert len(slaves) > 2
    assert all(isinstance(slave, sshtools.device.Device) for slave in slaves)
    assert master not in slaves

    master, slaves = sshtools.ssync.get_relevant_devices("thinkcentre", None, None)
    assert master == sshtools.device.Device("thinkcentre")
    assert len(slaves) > 2
    assert master not in slaves

    master, slaves = sshtools.ssync.get_relevant_devices(None, "laptop", "thinkcentre")
    assert master == sshtools.device.Device("laptop")
    assert slaves == [sshtools.device.Device("thinkcentre")]

    master, slaves = sshtools.ssync.get_relevant_devices(None, None, "serverpi")
    assert master == sshtools.device.Device.get_self()
    assert slaves == [sshtools.device.Device("serverpi")]

    master, slaves = sshtools.ssync.get_relevant_devices(None, "thinkcentre", None)
    assert master == sshtools.device.Device("thinkcentre")
    assert slaves == [sshtools.device.Device.get_self()]


def test_cmd():
    ssync = sshtools.ssync.Sync(
        sshtools.device.Device("laptop"),
        [sshtools.device.Device("oracle")],
        dry_run=True,
        connect=False,
    )
    with tempfile.TemporaryDirectory() as tmp_dir_obj:
        tmp_dir = Path(tmp_dir_obj)
        cmd = ssync.get_cmd(sshtools.device.Device("oracle"), tmp_dir)
        assert "--dry-run" in cmd
        assert cmd[0] == "rsync"
        assert isinstance(cmd, list)
        assert any(isinstance(c, str) for c in cmd)
