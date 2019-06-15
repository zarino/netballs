# Interesting links about DMX

## General explainers

* [Element14 – DMX Explained](https://www.element14.com/community/groups/open-source-hardware/blog/2017/08/24/dmx-explained-dmx512-and-rs-485-protocol-detail-for-lighting-applications)
* [Sparkfun – Introduction to DMX](https://learn.sparkfun.com/tutorials/introduction-to-dmx/all)
* [Instructables – How to Use DMX512 / RDM With Raspberry Pi](https://www.instructables.com/id/How-to-Use-DMX512-RDM-With-Raspberry-Pi/)
  * …Uses a [Zihatec RS485 HAT for Raspberry Pi](https://www.hwhardsoft.de/english/projects/rs485-shield/)

## DMX interfaces

* DMX interface board for Raspberry Pi, with input and output – <https://www.bitwizard.nl/shop/DMX-interface-for-Raspberry-pi>
* Enttec seem to have cornered the market on USB-to-DMX adaptors – <https://www.enttec.co.uk/product/protocols-gb/dmx512-gb/open-dmx-usb/> – fairly expensive.
* Chap using a Raspberry Pi to control lights via a cheap clone of an Enttec USB-to-DMX interface – <https://www.youtube.com/watch?v=ch0sNUbO9lo>

## RS485 interfaces

* [Zihatec RS485 HAT for Raspberry Pi](https://www.hwhardsoft.de/english/projects/rs485-shield/)
  * …Which was used in [this Instructables guide](https://www.instructables.com/id/How-to-Use-DMX512-RDM-With-Raspberry-Pi/)

## Raspberry Pi as DMX transmitter/controller ONLY

(Not quite what we’re after – we want Raspberry Pi to _receive_ DMX command over XLR cable.)

* QLC is Linux-based DMX controller software – <https://qlcplus.org/raspberry.html>
* “DiscoHAT” board sending DMX from a Raspberry Pi – <https://www.discohat.com/discohat/>
* Another example, using a Velleman USB-to-DMX interface [£61 on Amazon](https://www.amazon.co.uk/Velleman-K8062-Controlled-Interface-multicolored/dp/B000TA79UK) – <https://www.instructables.com/id/Raspberry-Pi-as-a-DMX-light-controller/>

## ESP32 as DMX receiver

* [Sparkfun –  Using Artnet DMX and the ESP32 to Drive Pixels](https://learn.sparkfun.com/tutorials/using-artnet-dmx-and-the-esp32-to-drive-pixels)

# I have no idea what this is all about, but it looks promising

* http://www.orangepi-dmx.org/
* https://github.com/vanvught/rpidmx512

# DMX lighting control software for Mac

* https://lightkeyapp.com/en/ – free as long as you need fewer than 24 channels
