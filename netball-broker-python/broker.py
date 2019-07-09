#!/usr/bin/env python

# -*- coding: utf-8 -*-

import random
import argparse
import serial
import time

import RPi.GPIO as GPIO
import paho.mqtt.publish as publish

parser = argparse.ArgumentParser(
    description='Receive lighting preset IDs over serial, and publish them to an MQTT server. Or, if manual mode is enabled through the hardware switch, publish the presets associated with the selected hardware buttons.'
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

# If manual mode isn't enabled, we'll take the numeric value sent
# over serial from the DMX Arduino, and translate it to values
# that the ESP32 can understand.
PRESETS = {
    # Black, with increasing amounts of sparkle.
    10: [0, 0, 0, 0, 0],
    11: [0, 0, 0, 0, 5],
    12: [0, 0, 0, 0, 10],
    13: [0, 0, 0, 0, 15],
    14: [0, 0, 0, 0, 25],
    15: [0, 0, 0, 0, 50],

    # Low power white, with increasing amounts of sparkle.
    20: [0, 0, 0, 255, 0],
    21: [0, 0, 0, 255, 5],
    22: [0, 0, 0, 255, 10],
    23: [0, 0, 0, 255, 15],
    24: [0, 0, 0, 255, 25],
    25: [0, 0, 0, 255, 50],

    # Ultra bright white - no need for sparkles here,
    # since all the pixels are already fully white.
    30: [255, 255, 255, 255, 0],

    # Blue, with increasing amounts of sparkle.
    40: [0, 0, 255, 0, 0],
    41: [0, 0, 255, 0, 5],
    42: [0, 0, 255, 0, 10],
    43: [0, 0, 255, 0, 15],
    44: [0, 0, 255, 0, 25],
    45: [0, 0, 255, 0, 50],

    # Gold, with increasing amounts of sparkle.
    50: [255, 125, 0, 0, 0],
    51: [255, 125, 0, 0, 5],
    52: [255, 125, 0, 0, 10],
    53: [255, 125, 0, 0, 15],
    54: [255, 125, 0, 0, 25],
    55: [255, 125, 0, 0, 50],

    # Pink, with increasing amounts of sparkle.
    60: [255, 0, 150, 0, 0],
    61: [255, 0, 150, 0, 5],
    62: [255, 0, 150, 0, 10],
    63: [255, 0, 150, 0, 15],
    64: [255, 0, 150, 0, 25],
    65: [255, 0, 150, 0, 50],

    # Purple, with increasing amounts of sparkle.
    70: [150, 0, 255, 0, 0],
    71: [150, 0, 255, 0, 5],
    72: [150, 0, 255, 0, 10],
    73: [150, 0, 255, 0, 15],
    74: [150, 0, 255, 0, 25],
    75: [150, 0, 255, 0, 50],
}

# If manual mode is enabled, these are the four colours
# which map to the four manual buttons.
MANUAL_PRESETS = {
    'BLUE': PRESETS[40],
    'GOLD': PRESETS[50],
    'PINK': PRESETS[60],
    'PURPLE': PRESETS[70],
}

current_manual_preset = None
manual_sparkle_active = False


# We store the colour state in here.
# R, G, B, W, Sparkle.
latest_rgbws = [0, 0, 0, 0, 0]


def main():
    if is_manual_mode_active():
        check_for_manual_data()
    else:
        check_for_serial_data()


def is_manual_mode_active():
    # Switch completes circuit when in "DMX" mode.
    return GPIO.input(SWITCH_MANUAL) == 0


def check_for_serial_data():
    global latest_rgbws

    serial_line = ser.readline().strip(' \rn')

    try:
        requested_preset = int(serial_line)
    except ValueError:
        if args.verbose:
            print "Non-numeric value received over serial: {}".format(serial_line)
        return False

    try:
        requested_rgbws = PRESETS[requested_preset]
    except KeyError:
        if args.verbose:
            print "Unknown preset requested: {}".format(requested_preset)
        return False

    if latest_rgbws != requested_rgbws:
        latest_rgbws = requested_rgbws
        publish_rgbws(latest_rgbws)
    else:
        ignore_rgbws(requested_rgbws)


def check_for_manual_data():
    global latest_rgbws
    global current_manual_preset
    global manual_sparkle_active

    # Store a flag, so know when the values have changed and need republishing.
    republish = False

    if is_blue_pressed() and current_manual_preset != 'BLUE':
        if args.verbose:
            print( "{} -> {}".format(current_manual_preset, 'BLUE') )
        current_manual_preset = 'BLUE'
        latest_rgbws = MANUAL_PRESETS[current_manual_preset]
        republish = True

    elif is_gold_pressed() and current_manual_preset != 'GOLD':
        if args.verbose:
            print( "{} -> {}".format(current_manual_preset, 'GOLD') )
        current_manual_preset = 'GOLD'
        latest_rgbws = MANUAL_PRESETS[current_manual_preset]
        republish = True

    elif is_pink_pressed() and current_manual_preset != 'PINK':
        if args.verbose:
            print( "{} -> {}".format(current_manual_preset, 'PINK') )
        current_manual_preset = 'PINK'
        latest_rgbws = MANUAL_PRESETS[current_manual_preset]
        republish = True

    elif is_purple_pressed() and current_manual_preset != 'PURPLE':
        if args.verbose:
            print( "{} -> {}".format(current_manual_preset, 'PURPLE') )
        current_manual_preset = 'PURPLE'
        latest_rgbws = MANUAL_PRESETS[current_manual_preset]
        republish = True

    if is_sparkle_pressed() and not manual_sparkle_active:
        # If Sparkle button is currently being held down, override
        # the default manual button's sparkle parameter, to 50.
        if args.verbose:
            print( "Sparkle active" )
        latest_rgbws[4] = 50
        manual_sparkle_active = True
        republish = True

    elif manual_sparkle_active and not is_sparkle_pressed():
        # Otherwise, reset the sparkle parameter back to the default
        # for the chosen manual colour.
        latest_rgbws[4] = MANUAL_PRESETS[current_manual_preset][4]
        manual_sparkle_active = False
        republish = True

    if republish:
        publish_rgbws(latest_rgbws)


def publish_rgbws(list_of_rgbws):
    latest_rgbws_string = list_as_string(list_of_rgbws)
    publish.single(
        "netball/all",
        latest_rgbws_string,
        hostname=args.server
    )
    if args.verbose:
        print "Published: {}".format( latest_rgbws_string )


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


def ignore_rgbws(list_of_rgbws):
    if args.verbose:
        print "Ignored: {}".format( list_as_string(list_of_rgbws) )


def list_as_string(list_of_things):
    return ' '.join(str(x) for x in list_of_things)


# Turn all the LEDs off (black) by default.
publish_rgbws(latest_rgbws)


# While loop and try/except lets us kill the script with ctrl-C.
while True:
    try:
        main()

    except KeyboardInterrupt as k:
        print ""
        break
