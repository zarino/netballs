#!/usr/bin/env python

# -*- coding: utf-8 -*-

from __future__ import division

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
# over serial from the DMX Arduino, and translate it to the RGBWS value
# at the given point in the routine.
#
# This list represents "sections" of the routine.
# First item is the percentage through the show that the section starts.
# Second item is the RGBWS DMX value at the start of that section.
# Note that half of our sections involve a smooth "fade" from one RGBWS to another!
SECTIONS = [
    (0,  [0, 0, 0, 0, 0]), # 0-5% black
    (5,  [0, 0, 0, 0, 0]), # 5-15% fade black <-> sparkles
    (15, [0, 0, 0, 0, 25]), # 15-20% sparkles
    (20, [0, 0, 0, 0, 25]), # 20-30% fade sparkles <-> blue
    (30, [0, 0, 255, 0, 25]), # 30-35% blue
    (35, [0, 0, 255, 0, 25]), # 35-45 fade blue <-> purple
    (45, [150, 0, 255, 0, 25]), # 45-50% purple
    (50, [150, 0, 255, 0, 25]), # 50-60% fade purple <-> pink
    (60, [255, 0, 150, 0, 25]), # 60-65% pink
    (65, [255, 0, 150, 0, 25]), # 65-75% fade pink <-> gold
    (75, [255, 125, 0, 0, 25]), # 75-80% gold
    (80, [255, 125, 0, 0, 25]), # 80-90% fade gold <-> white
    (90, [255, 255, 255, 255, 0]), # 90-95% white
    (95, [255, 255, 255, 255, 0]), # 95-100% fade white <-> black
    (100, [0, 0, 0, 0, 0]), # 100% black
]


# If manual mode is enabled, these are the four colours
# which map to the four manual buttons.
MANUAL_PRESETS = {
    'BLUE': SECTIONS[4][1],
    'PURPLE': SECTIONS[6][1],
    'PINK': SECTIONS[8][1],
    'GOLD': SECTIONS[10][1],
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
        serial_dmx_value = int(serial_line)
    except ValueError:
        if args.verbose:
            print "Non-numeric value received over serial: {}".format(serial_line)
        return False

    requested_rgbws = get_rgbws_for_dmx_value(serial_dmx_value)

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


def get_rgbws_for_dmx_value(xd):
    # Rough percentage that the engineer requested
    x = dmx_value_to_percent(xd)

    # The "section" of the routine that we're interested in.
    sec = max( i for i in range(len(SECTIONS)) if x >= SECTIONS[i][0] )

    # How far through the section we are, as a number between 0 and 1.
    a = (x - SECTIONS[sec][0]) / (SECTIONS[sec+1][0] - SECTIONS[sec][0])

    # Generate a smoothly faded rgbws value list, based on our progress between
    # the current section's rgbws value, and the next section's rgbws value.
    rgbws = [ int(p+a*(q-p)) for p, q in zip(SECTIONS[sec][1], SECTIONS[sec+1][1]) ]

    return rgbws


def dmx_value_to_percent(dmx_value):
    return (dmx_value / 256) * 100


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
