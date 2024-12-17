import os
import struct
from util import calculate_checksum


def create_icmp_packet():
    """Creates a raw ICMP echo request packet with checksum."""
    icmp_type = 8  # ICMP Echo Request type
    code = 0  # Code for echo request, usually set to 0
    checksum = 0  # Initial checksum value, will be replaced after calculation
    identifier = os.getpid() & 0xFFFF  # Use the process ID as the identifier (16-bit)
    sequence_number = 1  # Sequence number for tracking, starting at 1

    # Pack the header with a placeholder checksum (set to 0 initially)
    # `!BBHHH` format: '!' for network byte order, 2x unsigned char, 3x unsigned short
    header = struct.pack('!BBHHH', icmp_type, code, checksum, identifier, sequence_number)

    # Payload for the ICMP packet, here we use a 32-byte sample
    payload = b'abcdefghijklmnopqrstuvwabcdefghi'

    # Calculate the checksum on the header and payload together
    checksum = calculate_checksum(header + payload)

    # Repack the header with the correct checksum in place
    header = struct.pack('!BBHHH', icmp_type, code, checksum, identifier, sequence_number)

    # Return the complete packet, header plus payload
    return header + payload
