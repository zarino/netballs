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
args = parser.parse_args()

# Set up our serial receiver.
ser = serial.Serial(args.port, args.bitrate, timeout=1)

# This is the namespace our MQTT messages will start with.
topic_base = "netball/"

# These will get concatenated onto the end of topic_base.
channels = [
    "red",
    "green",
    "blue",
    "white",
    "sparkle",
]

# Turn a space-separated list of numbers (0-255)
# into a channel:number dictionary.
def extract_values(list_of_values):
    values = list_of_values.strip().split()
    return dict( zip(channels, values) )

# While loop and try/except lets us kill the script with ctrl-C.
while True:
    try:
        serial_line = ser.readline()
        for topic_suffix, value in extract_values(serial_line).items():
            publish.single(
                "{}{}".format(topic_base, topic_suffix),
                value,
                hostname=args.server
            )
    except KeyboardInterrupt as k:
        break
