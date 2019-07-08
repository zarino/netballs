#!/usr/bin/env python

import random
import argparse
import serial

import paho.mqtt.publish as publish

parser = argparse.ArgumentParser(
    description='Read space-separated lighting values from a serial, and publish them to an MQTT server'
)
parser.add_argument(
    '-p',
    '--port',
    default="/dev/ttyS0",
    help="Port on which to listen for input"
)
parser.add_argument(
    '-b',
    '--bitrate',
    default=9600,
    help="Bit rate of expected serial data"
)
parser.add_argument(
    '-s',
    '--server',
    default="netball-hub.local",
    help="MQTT server hostname to publish to"
)
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    default=False,
    help="Print messages to stdout in addition to sending over MQTT"
)
args = parser.parse_args()

# Set up our serial receiver.
ser = serial.Serial(args.port, args.bitrate, timeout=1)

# Starts off as an empty list, but will be filled
# the first time we receive values over serial.
latest_values = []


def publish_values(list_of_values):
    latest_values_string = list_as_string(list_of_values)
    publish.single(
        "netball/all",
        latest_values_string,
        hostname=args.server
    )
    if args.verbose:
        print "Published: {}".format( latest_values_string )


def ignore_values(list_of_values):
    if args.verbose:
        print "Ignored: {}".format( list_as_string(list_of_values) )


def list_as_string(list_of_things):
    return ' '.join(str(x) for x in list_of_things)


def string_as_list_of_ints(serial_line):
    return [ int(x) for x in serial_line.split() ]


# While loop and try/except lets us kill the script with ctrl-C.
while True:
    try:
        serial_line = ser.readline().strip(' \rn')
        incoming_values = string_as_list_of_ints(serial_line)

        if len(incoming_values) == 5:
            if latest_values != incoming_values:
                latest_values = incoming_values
                publish_values(latest_values)
            else:
                ignore_values(incoming_values)
        else:
            if args.verbose:
                print "Too short: {}".format(serial_line)

    except KeyboardInterrupt as k:
        print ""
        break
