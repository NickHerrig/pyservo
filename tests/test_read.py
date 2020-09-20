import pytest
from pyservo.read import *


@pytest.mark.parametrize(
    "test_packet,                      valid_checksum",[
     (bytearray(b'\x02\x91\x85\x98'),  True),
     (bytearray(b'\x02\x91\x85\x88'),  False),
])
def test_validate_checksum(test_packet, valid_checksum):
    assert validate_checksum(test_packet) == valid_checksum
