#!/usr/bin/env python

import argparse
import serial

parser = argparse.ArgumentParser(
    description='Print lines from serial port input'
)
parser.add_argument(
    '-p',
    '--port',
    default="/dev/ttyUSB0",
    help="Port on which to listen for input"
)
parser.add_argument(
    '-b',
    '--bitrate',
    default=9600,
    help="Bit rate of expected serial data"
)
args = parser.parse_args()

ser = serial.Serial(args.port, args.bitrate, timeout=1)
print(ser.name)

while True:
    try:
        serial_line = ser.readline()
        print( serial_line.strip() )
    except KeyboardInterrupt as k:
        print('')
        break

ser.close()
