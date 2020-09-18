import pytest
from pyservo.serial import *

@pytest.mark.parametrize(
    "test_packet,                     expected_checksum",[
     (bytearray([0x00, 0x00, 0x00]),  0x80)
])
def test_calculate_checksum(test_packet, expected_checksum):
    assert calculate_checksum(test_packet) == expected_checksum


@pytest.mark.parametrize(
    "test_data, expected_packet_length",[
     (0,          0x80),
     (-64,        0x80),
     (63,         0x80),
     (-15,        0x80),
     (15,         0x80),
     (-8192,      0xa0),
     (8191,       0xa0),
     (-100,       0xa0),
     (100,        0xa0),
     (-1048576,   0xc0),
     (1048575,    0xc0),
     (-9000,      0xc0),
     (9000,       0xc0),
     (-134217728, 0xe0),
     (134217727,  0xe0),
     (-2000000,   0xe0),
     (2000000,    0xe0),
])
def test_calculate_packet_length(test_data, expected_packet_length):
    assert calculate_packet_length(test_data) == expected_packet_length


@pytest.mark.parametrize(
    "test_data, expected_data_bytes",[
     (60,       [0xbc]),
     (-60,      [0xc4]),
     (120,      [0x80, 0xf8]),
     (-120,     [0xff, 0x88]),
     (9000,     [128, 198, 168]),
     (1200000,  [128, 201, 159, 128]),
])
def test_create_data_bytes(test_data, expected_data_bytes):
    assert create_data_bytes(test_data) == expected_data_bytes


@pytest.mark.parametrize(
    "func_code, data, expected_packet",[
     (0x00,     0,   bytearray([0x02, 0x80, 0x80, 0x82])),
])
def test_create_servo_packet(func_code, data, expected_packet):
    assert create_servo_packet(func_code, data) == expected_packet

