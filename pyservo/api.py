from .write import create_servo_packet
from .read import parse_return_packet


write_func_code_dict = {
    'Set_Origin':                0x00,
    'Go_Absolute_Pos':           0x01,
    'Go_Relative_Pos':           0x03,
    'Read_Drive_ID':             0x06,
    'Read_Drive_Config':         0x08,
    'RegisterRead_Drive_Status': 0x09,
    'Read_SpeedGain':            0x19,
    'Set_SpeedGain':             0x11,
    'General_Read':              0x0e,
    'Is_AbsPos32':               0x1b,
}

def read_position(s, data=write_func_code_dict['Is_AbsPos32']):
    func_code = write_func_code_dict['General_Read']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    response_packet = s.read(10)
    response = parse_return_packet(response_packet)
    return response

def read_status(s):
    func_code = write_func_code_dict['RegisterRead_Drive_Status']
    packet = create_servo_packet(func_code)
    bytes_written = s.write(packet)
    response_packet = s.read(10)
    response = parse_return_packet(response_packet)
    return response

def read_speed_gain(s):
    func_code = write_func_code_dict['Read_SpeedGain']
    packet = create_servo_packet(func_code)
    bytes_written = s.write(packet)
    response_packet = s.read(10)
    response = parse_return_packet(response_packet)
    return response

def set_origin(s):
    func_code = write_func_code_dict['Set_Origin']
    packet = create_servo_packet(func_code)
    bytes_written = s.write(packet)
    return "Set Current Position Zero  Successfully"

def set_speed_gain(s, data):
    func_code = write_func_code_dict['Set_SpeedGain']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    s.flush()
    return "Speed Set Successfully"

def send_to(s, data):
    func_code = write_func_code_dict['Go_Absolute_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    res = s.read(10)
    return "Moving towards position {data}".format(data=data)

def motor_forwards(s, data=130000000):
    func_code = write_func_code_dict['Go_Relative_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    res = s.read(10)
    return "Moving forward towards the end of the track."

def motor_backwards(s, data=-130000000):
    func_code = write_func_code_dict['Go_Relative_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    res = s.read(10)
    return "Moving motor backwards towards the start of the track."

def stop_motor(s, data=0):
    func_code = write_func_code_dict['Go_Relative_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    res = s.read(10)
    return "Successfully stopped the Motor"
