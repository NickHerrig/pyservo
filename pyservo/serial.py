from math import log
import os

import serial

"""
drive_id = One byte (Start byte) = Bn
 - The MSB bit of start byte is always zero, the other seven bits are used
   for the Drive ID number which is set from 0 ~ 63
 - The drive ID can only be set if the RS485/232 Net check box is not checked


packet length & functioncode = One byte = Bn-1
 - Bn-1 = 1 b6 b5 b4 b3 b2 b1 b0
 - The bit b6 and b5 are for the length of packet, expressed as:

         b6     b5        Total packet length(=n+1)
         0       0            4
         0       1            5
         1       0            6
         1       1            7

 - The bits b4~b0 are used for the packet function


data = One - Four bytes
- depending on the size of data for each funciton, 1-4 bytes are sent
- some function codes take no data, aka dummy data(0-127)
      n        Data                          Range Remark
      3      -64 ~ 63                        Only B1 is used
      4      -8,192 ~ 8,191                  Only B2, B1 are used
      5      -1,048,576 ~ 1,048,575          B3, B2, B1 are used
      6      -134,217,728 ~ 134,217,727      B4, B3, B2, B1 are used

checksum = One byte
 - S = B3 + B2 + B1 = 0x144 = 324 (First sum the packets)
 - B0 = 0x80 + Mod(S , 128) (Then calculate checksum B0)

"""

DRIVE_ID = int(os.environ['PYSERVO_DRIVE_ID'])
PORT = os.environ['PYSERVO_USB_PORT']


def calculate_checksum(packet):
    return 0x80 | ( sum(packet) & 0x7f )



def general_read():

    drive_id = DRIVE_ID
    func_code = 0x0e
    packet_length = 0x80
    byte_two = func_code | packet_length

    data = 0x80 | 0x1b

    packet = bytearray([drive_id, byte_two, data])

    checksum = calculate_checksum(packet)
    packet.append(checksum)

    return packet


def stop_motor():

    drive_id = DRIVE_ID
    func_code = 0x03
    packet_length = 0x80
    byte_two = func_code | packet_length

    data = 0x80  #Go to 0 - stop motor

    packet = bytearray([drive_id, byte_two, data])

    checksum = calculate_checksum(packet)
    packet.append(checksum)

    return packet


def main():
    s = serial.Serial(port=PORT,
                      baudrate=38400,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      bytesize=serial.EIGHTBITS,
                      timeout=1)

    print("Conntected to device:", s.name)
    packet = stop_motor()
    print("Writing packet:", packet)
    bytes_written = s.write(packet)
    response = s.read(10)

    s.close()
