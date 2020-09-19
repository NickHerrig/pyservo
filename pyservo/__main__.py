import os

import serial


if __name__ == '__main__':
    PORT = os.environ['PYSERVO_USB_PORT']

    s = serial.Serial(port=PORT,
                      baudrate=38400,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      bytesize=serial.EIGHTBITS,
                      timeout=1)

    print("Conntected to device:", s.name)

    from .cli import main
    main(s)

    s.close()
