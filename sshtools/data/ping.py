"""Module containing the executable class Ping for checking whether devices are alive."""

import datetime
import subprocess


class Ping:  # pylint: disable=R0903
    """
    An executable class that checks whether a device is alive and the latency to reach it.
    After the class is initialized with the target devices location, run Ping.ping() to obtain the information.
    """

    NUM_PINGS: int = 1
    IP_PING_TIMEOUT: float = 0.7

    target: str

    latency: datetime.timedelta
    alive: bool

    def __init__(self, target: str):
        self.target = target

    @staticmethod
    def _process_ping_result(
        ping_result: subprocess.CompletedProcess,
    ) -> (bool, datetime.timedelta):
        """
        The _process_ping_result function is a helper function that takes the result of a ping command and updates
        the alive and latency attributes of the Ping object.

        A device is alive if the return code from subprocess.CompletedProcess is 0.

        The latency of a device is the average of latency of the ping packets, as extracted from stdout.
        If the device is not alive, the latency will default the maximum value for datetime.timedelta.

        :param ping_result:subprocess.CompletedProcess: Stores the result of the ping command
        :returns: A tuple of a bool (is the device alive?) and a datetime.timedelta (latency)
        """
        if ping_result.returncode not in [0, 2]:
            raise ValueError(
                "The 'ping' command did not exit in valid state "
                f"(return code: {ping_result.returncode}; "
                f"stdout: {ping_result.stdout}; "
                f"stderr: {ping_result.stderr})"
            )

        alive = ping_result.returncode == 0

        if not alive:
            latency = datetime.timedelta.max
        else:
            stdout: str = str(ping_result.stdout)
            avg_latency_ms: float = float(
                stdout.rsplit("\n", maxsplit=1)[-1].split(" = ")[1].split("/")[1]
            )
            latency = datetime.timedelta(milliseconds=avg_latency_ms)
        return alive, latency

    def ping(self):
        """
        The ping function is used to determine if a device is alive and how long it takes for the device to respond.

        If no 'ping' executable is present, a FileNotFoundError will be raised.
        """
        which_ping_result = subprocess.run(
            ["which", "ping"], check=False, capture_output=True
        )
        if which_ping_result.returncode != 0:
            raise FileNotFoundError("No executable for 'ping' was found in the PATH.")

        ping_result: subprocess.CompletedProcess = subprocess.run(
            [
                "ping",
                "-q",  # be quiet
                f"-c {self.NUM_PINGS}",  # only try once
                self.target,
            ],
            capture_output=True,
            timeout=self.IP_PING_TIMEOUT,
            check=False,
        )
        self.alive, self.latency = self._process_ping_result(ping_result)
