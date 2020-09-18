import pytest
from pyservo.serial import *

@pytest.mark.parametrize(
    "test_packet,                     expected_checksum",[
     (bytearray([0x00, 0x00, 0x00]),  0x80)
])
def test_calculate_checksum(test_packet, expected_checksum):
    assert calculate_checksum(test_packet) == expected_checksum
