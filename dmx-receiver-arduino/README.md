# dmx-receiver-arduino

We have a cheap Arduino Uno clone, and a [Conceptinetics CTC-DRA-10-R2 DMX shield](https://www.tindie.com/products/Conceptinetics/dmx-shield-for-arduino-rdm-capable/).

The aim is to have the Uno read incoming DMX commands, on a configurable range of channels, and then send those commands to a connected Raspberry Pi, via SoftwareSerial, since the Arduino can’t send serial comms over USB when the DMX shield is attached.

We’ll use a [YF08E voltage translator](http://www.datasheetcafe.com/yf08e-pdf-datasheet-30695/) to protect the Raspberry Pi’s 3.3V GPIO from the Arduino’s 5V output.

## How to set up the Arduino

You need to install the Conceptinetics DMX Library onto your computer before you can compile the code.

1. Download the DMX library as a `.zip` file from <http://sourceforge.net/projects/dmxlibraryforar>
2. Install the library using one of the methods described at <https://www.arduino.cc/en/Guide/Libraries>.

If the DMX shield is in place on the Arduino Uno, make sure its `EN` jumper is in the "off" position (shown as `EN` with a line above it, ie: "NOT EN") when you are uploading code to the Arduino. The DMX shield communicates with the Arduino over serial, so you must turn the shield off (by setting the `EN` jumper to "off") to re-enable normal serial communication between your computer and the Arduino.

Once you’ve uploaded the code to the Arduino, remember re-activate the shield by turning the `EN` jumper to the "on" position (shown as `EN` without a line above it).

## How to set up the Raspberry Pi

See [../serial-monitor-test-python](../serial-monitor-test-python).

## How to connect the Arduino and the Pi, via the voltage translator

<https://pinout.xyz> will come in useful for identifying the Pi GPIO pins.

* Arduino pin 10 -> Voltage translator B1
* Arduino pin 11 -> Voltage translator B2
* Arduino 5V -> Voltage translator VB
* Arduino GND -> Voltage translator GND

* Raspberry Pi USB -> Arduino USB (for power, and common ground)

* Pi pin 1 -> Voltage translator VA
* Pi pin 8 -> Voltage translator A1
* Pi pin 10 -> Voltage translator A2

* Voltage translator VA -> Voltage translator OE

## Useful links

DMX shield

* https://forum.arduino.cc/index.php?topic=458860.0 – Someone with our exact DMX Shield, discovering that it hogs the Serial RX/TX lines on the Arduino, meaning you can’t use USB Serial input/output when the shield is active.

I2C – Pi as master, Arduino as slave

* https://raspberrypi.stackexchange.com/questions/62206/sending-and-receiving-string-data-between-arduino-and-raspberry-pi-using-the-i2c – Example of using `RPi.GPIO` Python module, to send I2C commands from a Raspberry Pi master to an Arduino slave, and then the Arduino `Wire` library to receive those commands.

I2C – Pi as slave, Arduino as master

* https://raspberrypi.stackexchange.com/questions/76109/raspberry-as-an-i2c-slave – Raspberry Pi as I2C slave
* https://www.raspberrypi.org/forums/viewtopic.php?t=235740 – Raspberry Pi as I2C slave
* https://oroboto.net/2018/10/21/arduino-with-raspberry-pi-i2c-slave/ – Example of using `pigpio` C-library, via the Python bindings, to send I2C commands from an Arduino master to a Raspberry Pi slave.

I2C on a Pi in general

* https://github.com/joan2937/pigpio – `pigpio` C-library, includes Python bindings.
* https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c – Configuring I2C on a Raspberry Pi.
* https://pinout.xyz/pinout/i2c – Pinout diagram showing location of I2C pins on Raspberry Pi.
* https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all – Nice clear example of using I2C on a Raspberry Pi (using `smbus` Python library).

I2C on an Arduino in general

* https://github.com/mcauser/i2cdetect – Arduino version of the Pi’s `i2cdetect` utility program, useful for showing I2C addresses of devices connected to the Arduino.

3.3V Pi GPIO vs 5V Arduino GPIO

* https://raspberrypi.stackexchange.com/questions/95430/5v-3-3v-sensors-confusion – Info about the danger of sending 5V signals to the Raspberry Pi’s 3V GPIO.
* https://www.raspberrypi-spy.co.uk/2018/09/using-a-level-shifter-with-the-raspberry-pi-gpio/ – voltage level shifting.
