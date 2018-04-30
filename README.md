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

The ``powerswitch_tx.py`` script is used to modify the state of the raspberry pi
switch. The basic usage is

```
$ powerswitch_tx.py -i $IP_ADDR -p $PORT -c $COMMAND
```

where ``$IP_ADDR`` is the IP of the server running ``powerswitch_rx.py``,
``$PORT`` is the port to send commands over, and ``$COMMAND`` is the command to
send to the server. The commands that can be sent are:

```
on              Turn the switch on.
off             Turn the switch off.
toggle          Toggle the switch state.
status          Read the switch state.
quit            Quit the server, can only be run locally.
```


Module
------

Most of the functionality of the receiver has been moved to a module in case
more specific usage is needed. This module is the file ``piswitch.py``. The
documentation for this module is done via the docstrings.

Installation
------------

All you need to do is run `python setup.py install` and the software will be
installed. The name of the script that recieves data from a socket is called
`powerswitch_rx.py`. Sending data to the switch is done with
`powerswitch_tx.py`.
