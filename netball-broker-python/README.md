# netball-broker-python

`broker.py` is the script that will eventually run on the Rasbperry Pi, reading (software) serial data from the connected Arduino Uno, and publishing them to its MQTT server.

`serial-debug.py` is a handy command line script for testing the Pi’s software serial connection – it just prints out any data received on the specified serial port.

## Running broker.py as a systemd background process, on boot

Git clone this repo onto the Raspberry Pi, and make sure you’ve installed the Python dependencies:

    cd /home/pi
    git clone https://github.com/zarino/netballs.git
    cd netballs/netball-broker-python/
    pip install -r requirements.txt

Copy the `netball-broker.service` file to the systemd directory:

    sudo cp /home/pi/netballs/netball-broker-python/netball-broker.service /lib/systemd/system/netball-broker.service
    sudo chmod 644 /lib/systemd/system/netball-broker.service

Note: If you’ve checked out the Git repo somewhere _other_ than `/home/pi/netballs` then you’ll need to amend the `ExecStart` line inside `netball-broker.service` to include the correct path to `broker.py`.

Once the `netball-broker.service` file has been copied, you can tell systemd to load it:

    sudo systemctl daemon-reload
    sudo systemctl enable netball-broker

Systemd will start the service at the next boot.

If you want to start the service _right now_, you can:

    sudo systemctl start netball-broker

Other systemd commands work as you’d expect:

    systemctl status netball-broker
    sudo systemctl stop netball-broker

And if you want to test it out by rebooting the Pi:

    sudo reboot

## Tips for debugging

You can publish and monitor MQTT messages using the [mosquitto command line programs](https://mosquitto.org/download/). This comes in handy when you want to send a test message, or you want to see which messages are already being sent.

On a Mac, you can get it via Homebrew:

    brew install mosquitto

Then, to publish a message:

    mosquitto_pub --host netball-hub.local --topic netball/red -m 255

And to monitor all messages:

    mosquitto_sub -v --host netball-hub.local --topic '#'
