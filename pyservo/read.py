
#TODO: Implement status data parser - def  parse_status(packet):

#TODO: Implement config data parser - def  parse_config(packet):

#TODO: Implement abs data parser - def  parse_config(packet):


read_func_codes_dict = {
    'Is_SpeedGain': 0x11,
}


def  parse_data(packet):
    func_code = packet[1] & 0x1f
    if func_code == 0x19:
        print("Is_Status parser not implemented yet.")
    elif func_code == 0x1a:
        print("Is_Config  parser not implemented yet.")
    elif func_code == 0x1b:
        print("Absolute Position parser not implemented yet.")
    elif func_code == 0x1e:
        print("Current Torque parser not implemented yet.")
    elif func_code in read_func_codes_dict.values():
        return packet[2] & 0b01111111


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
