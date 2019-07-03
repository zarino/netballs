import machine
import neopixel
import time
import random

number_of_leds = 40

input_red = 0
input_green = 0
input_blue = 255
input_white = 0
input_sparkle = 25

np = neopixel.NeoPixel(
    machine.Pin(13),
    number_of_leds,
    bpp=4
)

def sparkling(sparkle_chance):
    return sparkle_chance > 0 and input_sparkle >= random.randint(1, 256)

while True:
    for x in range(0, number_of_leds):
        if sparkling(input_sparkle):
            np[x] = (
                255,
                255,
                255,
                255,
            )
        else:
            np[x] = (
                input_red,
                input_green,
                input_blue,
                input_white,
            )

    np.write()
    time.sleep(0.02)
