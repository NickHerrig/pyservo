import pytest
from pyservo.serial import *

def test_calculate_checksum():
    packet = bytearray([0x00, 0x00, 0x00])
    assert calculate_checksum(packet) == 0x80
