import ipaddress
import socket
from contextlib import closing


def ip_to_int(ip):
    # Convert an IP address to an integer for comparison.
    return int(ipaddress.IPv4Address(ip))


def calculate_distance(ip1, ip2):
    # Define subnet masks (adjust as needed).
    subnet_mask_1 = 24  # /24 subnet mask
    subnet_mask_2 = 24  # /24 subnet mask

    # Convert IP addresses to integers.
    ip1_int = ip_to_int(ip1)
    ip2_int = ip_to_int(ip2)

    # Calculate subnet ranges.
    subnet_range_1 = (ip1_int >> (32 - subnet_mask_1)) << (32 - subnet_mask_1)
    subnet_range_2 = (ip2_int >> (32 - subnet_mask_2)) << (32 - subnet_mask_2)

    # Calculate the approximate distance based on the subnet ranges.
    distance = abs(subnet_range_1 - subnet_range_2) / 2 ** (32 - max(subnet_mask_1, subnet_mask_2))

    return distance


def sorted_ips(ip, ips):
    return sorted(ips, key=lambda ips_item: calculate_distance(ip, ips_item))


def find_available_port():
    for port in range(65535, 1024, -1):
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.bind(("127.0.0.1", port))
            yield port
        except OSError:
            pass


fap = find_available_port()
