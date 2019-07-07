import machine
import neopixel
import network
import time
import random

from minimalmdns import mdnshostnametoipnumber
from umqtt.robust import MQTTClient


number_of_leds = 60

wifi_ssid = 'netball-hub-wifi'
wifi_password = 'bubblino'
mqtt_broker_hostname = 'netball-hub.local'
mqtt_client_name = "{}{}".format('netball-esp32-', machine.unique_id())
mqtt_topic_base = "netball/"

channels = [
    "red",
    "green",
    "blue",
    "white",
    "sparkle",
]

state = {
    "red": 0,
    "green": 0,
    "blue": 0,
    "white": 0,
    "sparkle": 0,
}


# Set up neopixel string.
np = neopixel.NeoPixel(
    machine.Pin(4),
    number_of_leds,
    bpp=4
)


# The callback that handles MQTT messages.
def mqtt_message_callback(topic, msg):
    topic = topic.decode('utf-8')
    msg = msg.decode('utf-8').strip()
    print("MQTT message:", topic, msg)

    if topic.startswith(mqtt_topic_base):
        # Remove the mqtt_topic_base from the start of the topic,
        # leaving only the subtopic (eg: "red", "sparkle", or "all")
        channel = topic[len(mqtt_topic_base):]

        # A single channel/colour pair.
        if channel in channels:
            state[channel] = int(msg)

        # A request to change all channels at once.
        elif channel == 'all':
            values = msg.split()
            output = [0, 0, 0, 0, 0]
            # If only one colour provided, repeat that across red, green,
            # and blue channels (leaving white and sparkle empty).
            if len(values) == 1:
                values = values * 3
            for i, value in enumerate(values):
                output[i] = int(value)
            for i, key in enumerate(channels):
                state[key] = output[i]


# Magic.
def update_leds():
    for x in range(0, number_of_leds):
        if sparkling(state["sparkle"]):
            np[x] = (
                255,
                255,
                255,
                255,
            )
        else:
            np[x] = (
                state["red"],
                state["green"],
                state["blue"],
                state["white"],
            )

    np.write()


# Less or more likely to return True, based on the sparkle_chance.
# sparkle_chance of 0 means 0% chance of returning True.
# sparkle_chance of 255 means 100% chance of returning True.
def sparkling(sparkle_chance):
    return sparkle_chance > 0 and sparkle_chance >= random.randint(1, 256)


# Set all LEDs to the same colour. Useful for debugging.
def fill_all_leds(r, g, b, w):
    for x in range(0, number_of_leds):
        np[x] = (r, g, b, w)
    np.write()


# Clear LEDs before we start.
fill_all_leds(0, 0, 0, 0)


# Wait a little bit before we turn on wifi.
time.sleep(1.5)
wifi = network.WLAN(network.STA_IF)
wifi.active(True)


print("Connecting to", wifi_ssid)
fill_all_leds(0, 0, 255, 0) # blue


# Connect to the specified wifi network.
wifi.connect(wifi_ssid, wifi_password)
while not wifi.isconnected():
    time.sleep(0.1)


print("Connected to", wifi_ssid)
fill_all_leds(0, 255, 0, 0) # green
time.sleep(1)


print("Connecting to MQTT broker")
fill_all_leds(255, 150, 0, 0) # yellow
time.sleep(2)


# Find out the IP address of the MQTT broker.
if mqtt_broker_hostname[-6:] == ".local":
    print("Looking up MQTT broker IP address")
    mqtt_broker_ip = mdnshostnametoipnumber(wifi, mqtt_broker_hostname)
    print("mDNS completed:", mqtt_broker_hostname, "=", mqtt_broker_ip)
else:
    mqtt_broker_ip = mqtt_broker_hostname


# Connect to MQTT broker.
client = MQTTClient(mqtt_client_name, mqtt_broker_ip, 1883)
print("Connecting to MQTT broker", mqtt_broker_ip, "as client", mqtt_client_name)
for i in range(100):
    try:
        client.connect()
        break
    except OSError as e:
        print(e)
        fill_all_leds(255, 0, 0, 0)


print("Connected to MQTT broker", mqtt_broker_ip)
for i in range(0, 3):
    fill_all_leds(0, 0, 0, 0)
    time.sleep(0.3)
    fill_all_leds(0, 0, 0, 255)
    time.sleep(0.3)


# Reset LEDs again, ready for normal operation.
fill_all_leds(0, 0, 0, 0)


# Listen for MQTT messages.
client.set_callback(mqtt_message_callback)
client.subscribe( "{}#".format(mqtt_topic_base) )


while True:
    client.check_msg()
    update_leds()
    time.sleep_ms(25)
