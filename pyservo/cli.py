import argparse

def main(s):
    parser = argparse.ArgumentParser(
        description='Command line interface for reading and writing to DMM drive',
    )

    parser.add_argument('operation', help='operation to perform on servo, example: read_speed_gain')
    parser.add_argument('--data', action='store', type=int, default=4, help='data to pass to the servo motor, example: 60')

    args = parser.parse_args()

    if args.operation == 'read_speed_gain':
        from .api import read_speed_gain
        response = read_speed_gain(s)
        print(response)

    elif args.operation == 'set_speed_gain':
        from .api import set_speed_gain
        response = set_speed_gain(s, data=args.data)
        print(response)
    else:
        parser.print_help()


if __name__=='__main__':
    main()
