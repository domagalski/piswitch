PiSwitch
===========================================================

This is control code for a raspberry pi GPIO-based lightswitch.

Basic Usage
-------------

The hardware setup that his script itnerfaces with is a relay switch that
controls a power outlet. There aren't any huge specifics about what the hardware
needs to be, just a simple switch that plugs into GPIO pin 12 on the raspberry 
pi. The ``powerswitch_rx.py`` script runs on the pi. The basic usage of
``powerswitch_rx.py`` is

```
$ powerswitch_rx.py -p $PORT
```

where ``$PORT`` is whatever port that the script will be run on. This port needs
to be opened in the raspberry pi's firewall (if applicable) in order for
computers on the same local network to be able to send commands.

Installation
------------

All you need to do is run `python setup.py install` and the software will be
installed. The name of the script that recieves data from a socket is called
`powerswitch_rx.py`. Sending data to the switch is done with
`powerswitch_tx.py`.
