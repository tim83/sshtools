import datetime as dt
import time

import tabulate

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


def test_mt_map():
    src = [1, 2, 3]
    output = []
    tools.mt_map(lambda i: output.append(i**2), src)
    assert sorted(output) == [1, 4, 9]


def test_mt_map_timing():
    start_dt = dt.datetime.now()
    tools.mt_map(lambda i: time.sleep(0.5), 5 * "test")
    end_dt = dt.datetime.now()
    process_time: dt.timedelta = end_dt - start_dt
    assert process_time.total_seconds() < 1


def test_create_table():
    def add_row(output, row_data):
        output.append([row_data, row_data**2, row_data**3])

    headers = ["Number", "Square", "Cube"]
    created_table = tools.create_table(
        add_row, range(5), sorting_key=lambda r: -r[0], headers=headers
    )
    reference_table = tabulate.tabulate(
        [[4, 16, 64], [3, 9, 27], [2, 4, 8], [1, 1, 1], [0, 0, 0]], headers=headers
    )
    assert created_table == reference_table
