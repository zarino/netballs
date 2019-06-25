# dmx-receiver-arduino

We have a cheap Arduino Uno clone, and a [Conceptinetics CTC-DRA-10-R2 DMX shield](https://www.tindie.com/products/Conceptinetics/dmx-shield-for-arduino-rdm-capable/).

The aim is to have the Uno read incoming DMX commands, on a configurable range of channels, and then send those commands to a connected Raspberry Pi, most likely via a [YF08E voltage translator](http://www.datasheetcafe.com/yf08e-pdf-datasheet-30695/) and an [I2C connection](https://oscarliang.com/raspberry-pi-arduino-connected-i2c/), since Arduino can’t send serial comms over USB when the shield is attached.

Not sure yet whether the Arduino should be the I2C master (sending the latest DMX data to the Pi), or whether the Pi should be the master (sending _requests_ for the latest data to the Arduino). Will investigate.

## How to run this code

You need to install the Conceptinetics DMX Library onto your computer before you can compile the code.

1. Download the DMX library as a `.zip` file from <http://sourceforge.net/projects/dmxlibraryforar>
2. Install the library using one of the methods described at <https://www.arduino.cc/en/Guide/Libraries>.

If the DMX shield is in place on the Arduino Uno, make sure its `EN` jumper is in the "off" position (shown as `EN` with a line above it, ie: "NOT EN") when you are uploading code to the Arduino. The DMX shield communicates with the Arduino over serial, so you must turn the shield off (by setting the `EN` jumper to "off") to re-enable normal serial communication between your computer and the Arduino.

Once you’ve uploaded the code to the Arduino, remember re-activate the shield by turning the `EN` jumper to the "on" position (shown as `EN` without a line above it).

## Useful links

* https://forum.arduino.cc/index.php?topic=458860.0
* https://raspberrypi.stackexchange.com/questions/62206/sending-and-receiving-string-data-between-arduino-and-raspberry-pi-using-the-i2c
* https://www.raspberrypi-spy.co.uk/2018/09/using-a-level-shifter-with-the-raspberry-pi-gpio/
