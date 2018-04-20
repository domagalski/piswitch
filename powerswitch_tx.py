#!/usr/bin/env python2

import sys
import socket
import argparse

# convert words to one-character text commands
commands = ['off', 'on', 'toggle', 'quit']

if __name__ == '__main__':
    # Parse arguments from the user.
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command',
                        default='status',
                        help='Command to send to the receiver.')
    parser.add_argument('-i', '--ip',
                        required=True,
                        help='IP address of the receiver.')
    parser.add_argument('-p', '--port',
                        type=int,
                        required=True,
                        help='Port to communicate over.')
    args = parser.parse_args()
    addr = args.ip
    port = args.port
    command = args.command

    # Send command to UDP receiver.
    tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tx.sendto(command, (addr, port))

    # Receive status of the arduino power switch.
    status, _ = tx.recvfrom(1024)
    if status == 'err':
        if command == 'quit':
            print 'ERROR: Receiver can only be quit from localhost.'
        else:
            print 'ERROR: Invalid command:', command
        sys.exit(1)
    else:
        if command == 'quit':
            print 'Terminating the receiver.'
        else:
            print 'Status of switch:', status
