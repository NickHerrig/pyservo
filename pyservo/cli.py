import argparse

from .api import *

def main(s):

    s.flush()

    FUNCTION_MAP = {
        'stop':       stop_motor,
        'forward':    motor_forwards,
        'backwards':  motor_backwards,
        'status':     read_status,
        'position':   read_position,
        'send-to':    send_to,
        'set-origin': set_origin,
        'set-speed':  set_speed,
    }

    parser = argparse.ArgumentParser(
        description='Command line interface for reading and writing to DMM drive',
    )

    parser.add_argument(
        'command',
        choices=FUNCTION_MAP.keys(),
        help='operation to perform on servo, example: read_speed_gain',
    )

    parser.add_argument(
        '--data',
        action='store',
        type=int,
        help='data to pass to the servo motor, example: 60'
    )

    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]

    if args.data == None:
        response = func(s)
        print(response)
    else:
        response = func(s, data=args.data)
        print(response)
