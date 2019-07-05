# netball-broker-python

`broker.py` is the script that will eventually run on the Rasbperry Pi, reading (software) serial data from the connected Arduino Uno, and publishing them to its MQTT server.

`serial-debug.py` is a handy command line script for testing the Pi’s software serial connection – it just prints out any data received on the specified serial port.

## Tips for debugging

You can publish and monitor MQTT messages using the [mosquitto command line programs](https://mosquitto.org/download/). This comes in handy when you want to send a test message, or you want to see which messages are already being sent.

On a Mac, you can get it via Homebrew:

    brew install mosquitto

Then, to publish a message:

    mosquitto_pub --host netball-hub.local --topic netball/red -m 255

And to monitor all messages:

    mosquitto_sub -v --host netball-hub.local --topic '#'
