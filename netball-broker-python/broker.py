#!/usr/bin/env python

# -*- coding: utf-8 -*-

import random
import argparse
import serial
import time

import RPi.GPIO as GPIO
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

# Set up GPIO board numbering scheme.
GPIO.setmode(GPIO.BCM)

# Set up manual override buttons.
SWITCH_MANUAL = 12
BUTTON_BLUE = 6
BUTTON_GOLD = 13
BUTTON_PINK = 19
BUTTON_PURPLE = 16
BUTTON_SPARKLE = 22
GPIO.setup(SWITCH_MANUAL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_BLUE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_GOLD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PINK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PURPLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_SPARKLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Our predefined colours.
MANUAL_COLOURS = {
    'BLUE': [0, 50, 255, 0, 0],
    'GOLD': [255, 150, 0, 0, 0],
    'PINK': [255, 0, 0, 150, 0],
    'PURPLE': [255, 0, 255, 0, 0],
}

current_manual_colour = None
manual_sparkle_active = False


# We store the colour state in here.
# R, G, B, W, Sparkle.
latest_values = [0, 0, 0, 0, 0]


def main():
    if is_manual_mode_active():
        check_for_manual_data()
    else:
        check_for_serial_data()


def is_manual_mode_active():
    # Switch completes circuit when in "DMX" mode.
    return GPIO.input(SWITCH_MANUAL) == 0


def check_for_serial_data():
    global latest_values

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


def check_for_manual_data():
    global latest_values
    global current_manual_colour
    global manual_sparkle_active

    # Store a flag, so know when the values have changed and need republishing.
    republish = False

    if is_blue_pressed() and current_manual_colour != 'BLUE':
        if args.verbose:
            print( "{} -> {}".format(current_manual_colour, 'BLUE') )
        current_manual_colour = 'BLUE'
        latest_values = MANUAL_COLOURS[current_manual_colour]
        republish = True
    elif is_gold_pressed() and current_manual_colour != 'GOLD':
        if args.verbose:
            print( "{} -> {}".format(current_manual_colour, 'GOLD') )
        current_manual_colour = 'GOLD'
        latest_values = MANUAL_COLOURS[current_manual_colour]
        republish = True
    elif is_pink_pressed() and current_manual_colour != 'PINK':
        if args.verbose:
            print( "{} -> {}".format(current_manual_colour, 'PINK') )
        current_manual_colour = 'PINK'
        latest_values = MANUAL_COLOURS[current_manual_colour]
        republish = True
    elif is_purple_pressed() and current_manual_colour != 'PURPLE':
        if args.verbose:
            print( "{} -> {}".format(current_manual_colour, 'PURPLE') )
        current_manual_colour = 'PURPLE'
        latest_values = MANUAL_COLOURS[current_manual_colour]
        republish = True

    if is_sparkle_pressed() and not manual_sparkle_active:
        # If Sparkle button is currently being held down, override
        # the default manual button's sparkle parameter, to 50.
        if args.verbose:
            print( "Sparkle active" )
        latest_values[4] = 50
        manual_sparkle_active = True
        republish = True
    elif manual_sparkle_active and not is_sparkle_pressed():
        # Otherwise, reset the sparkle parameter back to the default
        # for the chosen manual colour.
        latest_values[4] = MANUAL_COLOURS[current_manual_colour][4]
        manual_sparkle_active = False
        republish = True

    if republish:
        publish_values(latest_values)


def publish_values(list_of_values):
    latest_values_string = list_as_string(list_of_values)
    publish.single(
        "netball/all",
        latest_values_string,
        hostname=args.server
    )
    if args.verbose:
        print "Published: {}".format( latest_values_string )


def is_blue_pressed():
    # Switch completes circuit when pressed.
    return GPIO.input(BUTTON_BLUE) == 1


def is_gold_pressed():
    # Switch *breaks* circuit when pressed.
    return GPIO.input(BUTTON_GOLD) == 0


def is_pink_pressed():
    # Switch completes circuit when pressed.
    return GPIO.input(BUTTON_PINK) == 1


def is_purple_pressed():
    # Switch *breaks* circuit when pressed.
    return GPIO.input(BUTTON_PURPLE) == 0


def is_sparkle_pressed():
    # Switch *breaks* circuit when pressed.
    return GPIO.input(BUTTON_SPARKLE) == 0


def ignore_values(list_of_values):
    if args.verbose:
        print "Ignored: {}".format( list_as_string(list_of_values) )


def list_as_string(list_of_things):
    return ' '.join(str(x) for x in list_of_things)


def string_as_list_of_ints(serial_line):
    return [ int(x) for x in serial_line.split() ]


# Turn all the LEDs off (black) by default.
publish_values(latest_values)


# While loop and try/except lets us kill the script with ctrl-C.
while True:
    try:
        main()

    except KeyboardInterrupt as k:
        print ""
        break
