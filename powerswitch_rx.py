#!/usr/bin/env python2

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
