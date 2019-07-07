# mqtt-led-controller-esp32

This MicroPython code tells the ESP32 how to:

1. Connect to the `netball-hub-wifi` network being broadcast by the [netball-hub](../netball-hub) Raspberry Pi.
2. Listen for MQTT messages on the `netball/…` topic, eg: `netball/red 255`
3. Translate those MQTT messages into control signals for the connected SK6812 LEDs.

## How to use this

### Install the serial driver onto your computer

Download and install the [CP210x USB-to-UART Bridge VCP serial driver](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) if you don’t already have it.

If you’re on a Mac, you’ll need to “Allow” the extension in System Preferences – your Mac will show you how. You won’t need to restart your Mac after the installation.

### Test communication with the board

The Arduino IDE is a quick way to test you can communicate with your board. You will need to [follow the first section of this guide](https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-mac-and-linux-instructions/) to install the ESP32 boards into the IDE’s Board Manager.

Zarino’s note: The first time I did this, I got an error when I tried to upload the “Wifi Scan” example code from the Arduino IDE to the board, for testing:

    serial.serialutil.SerialException: Could not configure port: (6, 'Device not configured’)

I read a quick fix is to hold down the BOOT button while the code was uploading, and that allowed the code to upload fine. But then I wasn’t getting any serial output. I tried pressing the BOOT and RST buttons, to no avail.

Unplugged and re-plugged the USB cable, and the ESP32 booted up and started writing serial to the Arduino Serial Monitor. Your mileage may vary.

### Flash the MicroPython firmware onto the board

You’ll probably also want to create a virtualenv to store the Python packages we’re about to install:

    cd mqtt-led-controller-esp32
    virtualenv .
    . bin/activate

Now install the Python packages:

    pip install -r requirements.txt

If you’re using a brand new EPS32, you’ll need to erase its flash memory:

    esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash

Now, [download the latest MicroPython firmware binary for the ESP32](https://micropython.org/download#esp32), and flash it onto the board using this command (remembering to replace `/path/to/esp32-blah-blah.bin` with the path of the firmware binary you just downloaded):

    esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART write_flash -z 0x1000 /path/to/esp32-blah-blah.bin

If you encounter any problems at this point, [check out the “Getting started with MicroPython on the ESP32“ tutorial here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) for troubleshooting advice.

To test the MicroPython firmware has been correctly installed, open a terminal emulator session to the ESP32. On a Mac, you can do this using `screen`:

    screen /dev/tty.SLAB_USBtoUART 115200

Press the `Return` key a few times, and you should be given a command prompt like `>>>`. If you type some simple Python in here (like `1+1`) you should get an answer (`2`).

You can exit the `screen` session by pressing `ctrl`–`A` then `ctrl`–`\`.


### Upload the `minimalmdns.py` package onto the board

The ESP32 has a very simple filesystem. By default, the Python path expects local packages to be in the `/lib` directory. So we’ll need to create that directory, and then copy our `minimalmdns.py` package into it.

You do both of these things with the `ampy` command, installed as part of the `pip install -r requirements.txt` line you ran earlier.

First create the `/lib` directory on the ESP32:

    ampy --port /dev/tty.SLAB_USBtoUART mkdir /lib

Now copy `minimalmdns.py` into that `/lib` directory:

    ampy --port /dev/tty.SLAB_USBtoUART put vendor/minimalmdns.py /lib/minimalmdns.py


### Upload `main.py` onto the board

The ESP32 will run `/boot.py` on startup (if the file exists) and then `/main.py`.

To upload `main.py` to the ESP32:

    ampy --port /dev/tty.SLAB_USBtoUART put main.py

### Send test MQTT messages

Run commands like this to control the ESP32:

    mosquitto_pub --host netball-hub.local --topic netball/red -m 255

### Open a Python terminal on the ESP32

To open a terminal session on the ESP32:

    screen /dev/tty.SLAB_USBtoUART 115200

Press Enter or `Ctrl`-`C` to get to a Python REPL prompt.

Press `Ctrl`-`A` then `Ctrl`-`\`, then `Y` to exit.

## Useful links

* https://learn.sparkfun.com/tutorials/micropython-programming-tutorial-getting-started-with-the-esp32-thing/all
* https://github.com/dphans/micropython-ide-vscode

* https://github.com/DoESLiverpool/what-does-health-look-like/blob/master/mqtt_neopixel_visualiser/mqtt_neopixel_visualiser.ino
* https://github.com/goatchurchprime/jupyter_micropython_developer_notebooks/blob/master/projects/mqtt2drumneopixel_mdns.ipynb

