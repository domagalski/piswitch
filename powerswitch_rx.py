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

import os
import sys
import time
import socket
import argparse
import piswitch
import RPi.GPIO as GPIO

if __name__ == '__main__':
    # Command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        type=int,
                        required=True,
                        help='Port to communicate over UDP.')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Enable verbose output.')
    args = parser.parse_args()

    # Check permissions
    if os.geteuid():
        print 'ERROR: This requires root privileges.'
        sys.exit(1)

    # Connect to the arduino
    switch = piswitch.Controller(args.port, args.verbose)

    try:
        while switch.relay():
            pass
    except KeyboardInterrupt:
        print
    finally:
        os.remove(switch.config)
        GPIO.cleanup()
