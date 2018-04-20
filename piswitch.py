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
        self.gpio_state = self.check_status()
        self.set_gpio()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        print "derp derp derp"
        if os.path.exists(value):
            if not os.path.isfile(value):
                raise IOError(value + ' is not a regular file.')
        self._config = value

    @property
    def gpio_state(self):
        return self._gpio_state

    @gpio_state.setter
    def gpio_state(self, value):
        if value == GPIO.LOW or value == GPIO.HIGH:
            self._gpio_state = value
        else:
            raise ValueError('Invalid GPIO state.')

    def check_status(self):
        """
        Check the status of the (existing) configuration file.
        """
        try:
            with open(self.config) as f:
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
