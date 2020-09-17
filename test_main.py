import pytest
from main import calculate_checksum

def test_calculate_checksum():
    packet = bytearray([0x00, 0x00, 0x00])
    assert calculate_checksum(packet) == 0x80
