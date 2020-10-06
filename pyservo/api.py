from .write import create_servo_packet
from .read import parse_return_packet


write_func_code_dict = {
    'Set_Origin':                0x00,
    'Go_Absolute_Pos':           0x01,
    'Go_Relative_Pos':           0x03,
    'Set_TrqCons':               0x13,
    'Set_HighSpeed':             0x14,
    'Set_HighAccel':             0x15,
    'RegisterRead_Drive_Status': 0x09,
    'General_Read':              0x0e,
    'Is_AbsPos32':               0x1b,
    'Set_GearNumber':            0x17,
}

def set_torque(s, data=127):
    func_code = write_func_code_dict['Set_TrqCons']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Set torque to {data}.".format(data=data)

def set_acceleration(s, data):
    func_code = write_func_code_dict['Set_HighAccel']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Set acceleration to {data}.".format(data=data)

def set_gear_number(s, data):
    func_code = write_func_code_dict['Set_GearNumber']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Set Gear Number to {data}.".format(data=data)

def set_speed(s, data):
    func_code = write_func_code_dict['Set_HighSpeed']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Speed set to {data}".format(data=data)

def read_position(s, data=write_func_code_dict['Is_AbsPos32']):
    func_code = write_func_code_dict['General_Read']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    response = parse_return_packet(return_packet)
    return response

def read_status(s):
    func_code = write_func_code_dict['RegisterRead_Drive_Status']
    packet = create_servo_packet(func_code)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    response = parse_return_packet(return_packet)
    return response

def set_origin(s):
    func_code = write_func_code_dict['Set_Origin']
    packet = create_servo_packet(func_code)
    bytes_written = s.write(packet)
    s.flush()
    return "Set Current Position Zero  Successfully"

def send_to(s, data):
    func_code = write_func_code_dict['Go_Absolute_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Moving towards position {data}".format(data=data)

def motor_forward(s, data=130000000):
    func_code = write_func_code_dict['Go_Relative_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Moving forward towards the end of the track."

def motor_backward(s, data=-130000000):
    func_code = write_func_code_dict['Go_Relative_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Moving motor backwards towards the start of the track."

def stop_motor(s, data=0):
    func_code = write_func_code_dict['Go_Relative_Pos']
    packet = create_servo_packet(func_code, data)
    bytes_written = s.write(packet)
    return_packet = s.readline()
    print(return_packet)
    return "Successfully stopped the Motor"
