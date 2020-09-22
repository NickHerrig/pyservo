

def  parse_status_data(data_byte):
    """
    Documentation: http://www.dmm-tech.com/Files/DYN4MS-ZM7-A10A.pdf
    Page: 53

    Status = x b6 b5 b4 b3 b2 b1 b0

    b0 = 0 : On position, i.e. |Pset - Pmotor| < = OnRange
    b0 = 1 : motor busy, or |Pset - Pmotor|> OnRange
    b1 = 0 : motor servo
    b1 = 1 : motor free
    b4 b3 b2 = 0 : No alarm
     1 : motor lost phase alarm, |Pset - Pmotor|>8192(steps), 180(deg)
     2 : motor over current alarm
     3 : motor overheat alarm, or motor over power
     4 : there is error for CRC code check, refuse to accept current command
     5~ 7 : TBD
    b5 = 0 : means buit in S-curve, linear, circular motion completed; waiting for next motion
    b5 = 1 : means buit in S-curve, linear, circular motion is busy on current motion
    b6 : pin2 status of JP3,used for Host PC to detect CNC zero position or others
    """
    servo_status = {}
    if (data_byte >> 6) & 1 == 0:
        servo_status['pin2'] = '0'
    elif (data_byte >> 6) & 1 == 1:
        servo_status['pin2'] = '1'

    if (data_byte >> 5) & 1 == 0:
        servo_status['motion'] = 'completed'
    elif (data_byte >> 5) & 1 == 1:
        servo_status['motion'] = 'busy'

    if (data_byte >> 2) & 0b111 == 0:
        servo_status['alarm'] = 'no alarm'
    elif (data_byte >> 2) & 0b111 == 1:
        servo_status['alarm'] = 'lost phase'
    elif (data_byte >> 2) & 0b111 == 2:
        servo_status['alarm'] = 'over current'
    elif (data_byte >> 2) & 0b111 == 3:
        servo_status['alarm'] = 'overheat/overpower'
    elif (data_byte >> 2) & 0b111 == 4:
        servo_status['alarm'] = 'rcr error'
    elif (data_byte >> 2) & 0b111 > 4:
        servo_status['alarm'] = 'TBD'

    if (data_byte >> 1) & 1 == 0:
        servo_status['motor'] = 'servo'
    elif (data_byte >> 5) & 1 == 1:
        servo_status['motor'] = 'free'

    if data_byte & 1 == 0:
        servo_status['position'] = 'on position'
    if data_byte & 1 == 1:
        servo_status['position'] = 'busy'

    return servo_status


def sign_extend(value, bits):
    # from: https://stackoverflow.com/a/32031543
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def parse_signed_data(data_bytes):
    position = sign_extend(data_bytes[0] << 1, 8) >> 1
    for byte in data_bytes[1:]:
        position = (position << 7) + (byte & 0x7f)
    return  position

read_func_codes_dict = {
    'Is_SpeedGain': 0x11,
    'Is_Status':    0x19,
    'Is_AbsPos32':  0x1b,
}


def  parse_data(packet):
    func_code = packet[1] & 0x1f
    if func_code == read_func_codes_dict['Is_Status']:
        return parse_status_data(packet[2])
    # elif func_code == 0x1a:
    #     print("Is_Config  parser not implemented yet.")
    elif func_code == read_func_codes_dict['Is_AbsPos32']:
        return parse_signed_data(packet[2:-1])
    #     print("Absolute Position parser not implemented yet.")
    # elif func_code == 0x1e:
    #    print("Current Torque parser not implemented yet.")
    elif func_code in read_func_codes_dict.values():
        return packet[2] & 0b01111111
    else:
        return "Cannot recognized function code:{func_code}".format(func_code=func_code)


def validate_checksum(packet):
    checksum_byte = packet[-1]
    remaining_bytes = packet[:-1]
    checksum = 0x80 | ( sum(remaining_bytes) & 0x7f )

    if checksum_byte == checksum:
        return True
    else:
        return False


def parse_return_packet(packet):
    if validate_checksum(packet):
        return parse_data(packet)
    else:
        Print("error in packet, checksum is not valid.")
        return
