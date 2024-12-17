import os
import socket
import struct
import sys
import time

from client import HTTPConnection
from icmp import create_icmp_packet


def is_host_online(ip_address: str, timeout: int = 2) -> bool:
    """
    Checks if a host is online by sending an ICMP echo request.

    :param ip_address: IP address of the host.
    :param timeout: Timeout in seconds for waiting for a response.
    :return: True if the host is online, False otherwise.
    """
    # Create a raw socket specifically for sending ICMP packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    try:
        # Set the timeout on the socket to the specified value
        sock.settimeout(timeout)

        # Create an ICMP echo request packet
        packet = create_icmp_packet()

        # Send the ICMP packet to the target IP address, with port set to 0 (not used)
        sock.sendto(packet, (ip_address, 0))

        # Wait for a response from the target
        response, _ = sock.recvfrom(1024)  # 1024 bytes should be sufficient to capture the response

        # Extract the ICMP header from the response, which is located after the IP header
        # (IP header is typically 20 bytes, so ICMP header starts at byte 20)
        icmp_header = response[20:28]

        # Unpack the ICMP header fields
        # `!BBHHH` format unpacks to (type, code, checksum, identifier, sequence number)
        r_type, r_code, _, r_id, _ = struct.unpack('!BBHHH', icmp_header)

        # Check that we received an Echo Reply (type 0) and the identifier matches
        # We compare the received identifier (`r_id`) to the process ID to ensure the response is for our request
        if r_type == 0 and r_id == (os.getpid() & 0xFFFF):
            return True  # Host is online if we received a valid response
        return False  # Otherwise, the host is considered offline
    except (socket.error, socket.timeout):
        # Handle cases where no response is received within the timeout
        print(f"Request timed out for {ip_address}")
        return False
    finally:
        # Close the socket after the operation completes
        sock.close()


def get_open_ports(ip_address: str, ports: list, timeout: int = 1) -> list:
    """
    Checks which ports are open in the specified ports on a given IP address.

    :param ip_address: IP address of the host.
    :param ports: A list of ports that will be checked.
    :param timeout: Timeout in seconds for each connection attempt.
    :return: A list of open ports.
    """
    # List to store open ports
    open_ports = []

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            # Try connecting to the current port
            result = sock.connect_ex((ip_address, port))
            # If result is 0, the port is open
            if result == 0:
                open_ports.append(port)

    return open_ports


def get_open_ports_in_range(ip_address: str, port1: int, port2: int, timeout: int = 1) -> list:
    """
    Checks which ports are open between the specified two ports on a given IP address.

    :param ip_address: IP address of the host.
    :param port1: The first port in the range (inclusive).
    :param port2: The second port in the range (inclusive).
    :param timeout: Timeout in seconds for each connection attempt.
    :return: A list of open ports within the specified range.
    """
    # Ensure port1 is less than or equal to port2 to handle any order given
    start_port = min(port1, port2)
    end_port = max(port1, port2)

    return get_open_ports(ip_address, list(range(start_port, end_port + 1)), timeout)


def get_response_time(ip_address: str, port: int, timeout: int = 5) -> float:
    """
    Measures the response time to connect to a given IP address and port.

    :param ip_address: IP address of the host.
    :param port: Port number to check.
    :param timeout: Timeout in seconds for the connection attempt.
    :return: Response time in milliseconds, or -1 if the connection fails.
    """
    try:
        # Start timing with timeit.default_timer
        start_time = time.perf_counter()

        # Create a socket and attempt connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((ip_address, port))

        # End timing with timeit.default_timer
        end_time = time.perf_counter()

        # Calculate the response time in milliseconds
        response_time = (end_time - start_time) * 1000
        return response_time
    except (socket.timeout, socket.error):
        # Return -1 to indicate failure in connection
        return -1


def main():
    # nmap.py -status [ip address] *[ports]
    # nmap.py -status [ip address] -r [s port] [e port]
    # nmap.py -status 8.8.8.8 -r 40 80

    # nmap.py -latency [ip address] [port]
    # nmap.py -latency 8.8.8.8 80

    # nmap.py -curl [ip address] [port] -GET [id]
    # nmap.py -curl [ip address] [port] -POST [name] [age]
    # nmap.py -curl 127.0.0.1 8080 -GET 1
    # nmap.py -curl 127.0.0.1 8080 -POST yabal 21
    flag = sys.argv[1][1:]
    ip_address = sys.argv[2]
    port = sys.argv[3]

    if flag == "curl":
        con = HTTPConnection(ip_address, int(port))
        method = sys.argv[4][1:]

        if method == "GET":
            print(con.get_request(int(sys.argv[5])))
        elif method == "POST":
            print(con.post_request(sys.argv[5], int(sys.argv[6])))

    elif flag == "latency":
        response_time = get_response_time(ip_address, int(port))
        if response_time != -1:
            print(f"Response time: {response_time:.2f} ms")
        else:
            print("Could not connect to the host.")

    elif flag == "status":
        if not is_host_online(ip_address):
            print(f"{ip_address} is offline or unreachable.")
            return

        print(f"{ip_address} is online.")

        if port != "-r":
            print(f"open ports: {get_open_ports(ip_address, list(map(int, sys.argv[4:])))}")
        else:
            start_port = int(sys.argv[4])
            end_port = int(sys.argv[5])
            print(f"open ports: {get_open_ports_in_range(ip_address, start_port, end_port)}")


if __name__ == '__main__':
    main()
