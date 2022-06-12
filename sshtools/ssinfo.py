"""Obtain information about devices"""
import argparse

import timtools.log

import sshtools.device
import sshtools.ip
import sshtools.tools


def print_ips(device: sshtools.device.Device):
    """Print information about the IP addresses"""
    print(f"=== IPs of {device} ===")

    def ip_add_row(
        output: list[list[str, bool, float, bool, bool]],
        ip_address: sshtools.ip.IPAddress,
    ):
        row = [
            str(ip_address),
            ip_address.is_alive,
            ip_address.latency,
            ip_address.is_sshable(),
        ]
        output.append(row)

    table = sshtools.tools.create_table(
        ip_add_row,
        device.get_possible_ips(),
        sorting_key=lambda r: r[2],
        headers=["IP Address", "Reachable", "Latency (ms)", "SSHable?"],
    )
    print(table)


def run():
    """Run ssinfo"""
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("device", help="Computer die bestueerd moet worden")
    parser.add_argument("-v", "--verbose", help="Geef feedback", action="store_true")
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    device = sshtools.device.Device(args.device)
    print_ips(device)


if __name__ == "__main__":
    run()
