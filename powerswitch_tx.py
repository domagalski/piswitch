#!/usr/bin/env python2

# piswitch is control code for a raspberry pi GPIO-based lightswitch.
# Copyright (C) 2018    Rachel Simone Domagalski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    tx.settimeout(5)
    tx.sendto(command, (addr, port))

    # Receive status of the arduino power switch.
    try:
        status, _ = tx.recvfrom(1024)
    except socket.timeout:
        print 'ERROR: Cannot receive packets from server.'
        sys.exit(1)
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
