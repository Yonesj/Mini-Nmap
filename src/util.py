import array
import struct

# Define an endianness transform based on system architecture
# The `struct.pack("H", 1)` creates a 2-byte representation of the integer 1.
# If the output is `b"\x00\x01"`, the system is big-endian.
if struct.pack("H", 1) == b"\x00\x01":  # big endian
    # If big-endian, no transformation is needed.
    checksum_endian_transform = lambda chk: chk
else:
    # For little-endian systems, swap the bytes of the checksum.
    checksum_endian_transform = lambda chk: ((chk >> 8) & 0xff) | (chk << 8)


def calculate_checksum(data):
    """
    Calculates the checksum for the given data using the ICMP algorithm.
    :param data: The packet data as bytes.
    :return: Calculated checksum as an integer.
    """
    # If the length of data is odd, add a null byte to make it even
    if len(data) % 2 == 1:
        data += b'\0'

    # Sum the data as 16-bit words using an array of unsigned short integers
    # "H" format means unsigned short (16-bit), which ensures we're summing correctly
    checksum = sum(array.array("H", data))

    # Add carryover from high bits to low bits by moving bits above 16th back to the lower part
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += checksum >> 16  # Add any remaining carry if still greater than 16 bits

    # Apply a bitwise negation to finalize the checksum
    checksum = ~checksum

    # Apply endianness transform for system compatibility and return only lower 16 bits
    return checksum_endian_transform(checksum) & 0xffff
