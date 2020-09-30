import pytest
from pyservo.read import *


@pytest.mark.parametrize(
    "test_byte,     expected_integer",[
    (0b11111111,    -1),
    (0b01111111,    127),
    (0b10000010,    -126),
    (0b00000010,    2),
])
def test_sign_extend(test_byte, expected_integer):
    assert sign_extend(test_byte, 8) == expected_integer

@pytest.mark.parametrize(
    "test_data_bytes,         expected_integer",[
    (bytearray(b'\xd0\xc2'),  -6078),
])
def test_parse_signed_data(test_data_bytes, expected_integer):
    assert parse_signed_data(test_data_bytes) == expected_integer


@pytest.mark.parametrize(
    "test_status_byte, expected_status",[
    (0b10000000,       {
                           'pin2': '0',
                           'motion':'completed',
                           'alarm': 'no alarm',
                           'motor': 'servo',
                           'position': 'on position',}),
    (0b11100111,       {
                           'pin2': '1',
                           'motion':'busy',
                           'alarm': 'lost phase',
                           'motor': 'free',
                           'position': 'busy',}),
    (0b11101011,       {
                           'pin2': '1',
                           'motion':'busy',
                           'alarm': 'over current',
                           'motor': 'free',
                           'position': 'busy',}),
    (0b11101111,       {
                           'pin2': '1',
                           'motion':'busy',
                           'alarm': 'overheat/overpower',
                           'motor': 'free',
                           'position': 'busy',}),
    (0b11110011,       {
                           'pin2': '1',
                           'motion':'busy',
                           'alarm': 'rcr error',
                           'motor': 'free',
                           'position': 'busy',}),
    (0b11110111,       {
                           'pin2': '1',
                           'motion':'busy',
                           'alarm': 'TBD',
                           'motor': 'free',
                           'position': 'busy',}),
    (0b11111011,       {
                           'pin2': '1',
                           'motion':'busy',
                           'alarm': 'TBD',
                           'motor': 'free',
                           'position': 'busy',}),
])
def test_parse_status_data(test_status_byte, expected_status):
    status = parse_status_data(test_status_byte)
    assert status['pin2'] == expected_status['pin2']
    assert status['motion'] == expected_status['motion']
    assert status['alarm'] == expected_status['alarm']
    assert status['motor'] == expected_status['motor']
    assert status['position'] == expected_status['position']


@pytest.mark.parametrize(
    "test_packet,                      valid_checksum",[
    (bytearray(b'\x02\x91\x85\x98'),  True),
    (bytearray(b'\x02\x91\x85\x88'),  False),
])
def test_validate_checksum(test_packet, valid_checksum):
    assert validate_checksum(test_packet) == valid_checksum
