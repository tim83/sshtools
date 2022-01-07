import datetime as dt
import time

from sshtools import tools


def test_mt_filter_result():
    src = [1, 2, 3, 4, 5]
    res = [1, 2, 3]
    assert tools.mt_filter(lambda i: i <= 3, src) == res


def test_mt_filter_timing():
    start_dt = dt.datetime.now()
    tools.mt_filter(lambda i: time.sleep(0.5), 5 * "test")
    end_dt = dt.datetime.now()
    process_time: dt.timedelta = end_dt - start_dt
    assert process_time.total_seconds() < 1
