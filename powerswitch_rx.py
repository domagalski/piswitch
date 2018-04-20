#!/usr/bin/env python2

import os
import sys
import time
import socket
import argparse
import RPi.GPIO as GPIO


class Controller():
    """
    GPIO communication class.
    """
    def __init__(self, port, verbose):
        """
        Initialize the GPIO.
        """
        self.verbose = verbose

        self.rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx.bind(('', port))
        if self.verbose:
            print 'Receiver socket bound to port:', port

        # Pins used for the two switches
        self.gpio_pin = 12
        if self.verbose:
            print 'GPIO pin controlling the outlet:', self.gpio_pin

        # Set up the GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        # Load the configuration file. If it does not exist, create it
        self.config = '/usr/local/etc/powerswitch.status'
        self.gpio_state = GPIO.LOW
        if os.path.exists(self.config):
            if os.path.isfile(self.config):
                self.gpio_state = self.check_status()
            else:
                raise IOError(self.config + ' is not a regular file.')

        # Make sure pins are off by default.
        self.set_gpio()

    def check_status(self):
        """
        Check the status of the (existing) configuration file.
        """
        with open(self.config) as f:
            try:
                prev_status = int(f.read()[0])
            except:
                prev_status = GPIO.LOW
        return prev_status

    def relay(self):
        """
        Receive commands via UDP.
        Send commands to the arduino.
        Send back the result to the client.
        """
        # Receive command from socket.
        command, addr = self.rx.recvfrom(1024)
        command = command.replace('\n', '') # for interactive transmitters.
        if command not in ['on', 'off', 'toggle', 'status', 'quit']:
            print 'WARNING: Skipping invalid command:', command
            self.rx.sendto('err', addr)
            return True
        if command == 'quit' and addr[0] == '127.0.0.1':
            self.rx.sendto('quit', addr)
            if self.verbose:
                print 'Terminating the receiver',
                print time.asctime().join(['(', ')']) + '.'
            return False
        elif command == 'quit':
            self.rx.sendto('err', addr)
            if self.verbose:
                print 'Received invalid quit command from:', addr[0],
                print time.asctime().join(['(', ')'])
            return True
        if self.verbose:
            print 'Received', command, 'command from:', addr[0],
            print time.asctime().join(['(', ')'])

        # Send command to the arduino and return results to sender.
        if command == 'on':
            self.gpio_state = GPIO.HIGH
        elif command == 'off':
            self.gpio_state = GPIO.LOW
        elif command == 'toggle':
            self.gpio_state = int(not self.gpio_state)
        if command != 'status':
            self.set_gpio()

        status = 'on' if self.gpio_state == GPIO.HIGH else 'off'
        self.rx.sendto(status, addr)

        # Print arduino status and exit true to continue receiver loop.
        if self.verbose:
            print 'Status of GPIO pin', str(self.gpio_pin) + ':', status
        return True

    def set_gpio(self):
        """
        Set the GPIO and write down the status.
        """
        GPIO.output(self.gpio_pin, self.gpio_state)
        with open(self.config, 'w') as f:
            f.write(str(self.gpio_state))
            f.write('\n')

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
    switch = Controller(args.port, args.verbose)

    try:
        while switch.relay():
            pass
    except KeyboardInterrupt:
        print
    finally:
        os.remove(switch.config)
        GPIO.cleanup()
