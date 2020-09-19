from .write import create_servo_packet


func_code_dict = {
    'Set_Origin':        0x00,
    'Go_Absolute_Pos':   0x01,
    'Go_Relative_Pos':   0x03,
    'Read_Drive_ID':     0x06,
    'Read_Drive_Config': 0x08,
    'Read_SpeedGain':    0x19,
    'Set_SpeedGain':     0x11,
}


def read_speed_gain(s):
    func_code = func_code_dict['Read_SpeedGain']
    packet = create_servo_packet(func_code, 1)

    s.write(packet)
    response = s.read(8)

    return response


def set_speed_gain(s, data):
    func_code = func_code_dict['Set_SpeedGain']
    packet = create_servo_packet(func_code, data)

    s.write(packet)
    response = s.read(8)

    return response
