# Interesting links about DMX

## General explainers

* [Element14 – DMX Explained](https://www.element14.com/community/groups/open-source-hardware/blog/2017/08/24/dmx-explained-dmx512-and-rs-485-protocol-detail-for-lighting-applications)
* [Sparkfun – Introduction to DMX](https://learn.sparkfun.com/tutorials/introduction-to-dmx/all)
* [Instructables – How to Use DMX512 / RDM With Raspberry Pi](https://www.instructables.com/id/How-to-Use-DMX512-RDM-With-Raspberry-Pi/)
  * …Uses a [Zihatec RS485 HAT for Raspberry Pi](https://www.hwhardsoft.de/english/projects/rs485-shield/)

## DMX interfaces

* [Bitwizard DMX interface board for Raspberry Pi](https://www.bitwizard.nl/shop/DMX-interface-for-Raspberry-pi) – with input and output
* Enttec seem to have cornered the market on USB-to-DMX adaptors – <https://www.enttec.co.uk/product/protocols-gb/dmx512-gb/open-dmx-usb/> – fairly expensive.
* Chap using a Raspberry Pi to control lights via a cheap clone of an Enttec USB-to-DMX interface – <https://www.youtube.com/watch?v=ch0sNUbO9lo>
* A completely DIY DMX interface, using an Arduino – <https://www.instructables.com/id/Build-Your-Own-DMX-Fixture-Arduino/>

## RS485 interfaces

* [Zihatec RS485 HAT for Raspberry Pi](https://www.hwhardsoft.de/english/projects/rs485-shield/)
  * …Which was used in [this Instructables guide](https://www.instructables.com/id/How-to-Use-DMX512-RDM-With-Raspberry-Pi/)
* <https://www.instructables.com/id/DMX-512-to-Serial-Adapter/>

## Raspberry Pi as DMX transmitter/controller ONLY

(Not quite what we’re after – we want Raspberry Pi to _receive_ DMX command over XLR cable.)

* QLC is Linux-based DMX controller software – <https://qlcplus.org/raspberry.html>
* “DiscoHAT” board sending DMX from a Raspberry Pi – <https://www.discohat.com/discohat/>
* Another example, using a Velleman USB-to-DMX interface [£61 on Amazon](https://www.amazon.co.uk/Velleman-K8062-Controlled-Interface-multicolored/dp/B000TA79UK) – <https://www.instructables.com/id/Raspberry-Pi-as-a-DMX-light-controller/>
* ["Tinkerkit" Arduino DMX Master Shield at RS Components](https://uk.rs-online.com/web/p/processor-microcontroller-development-kits/7798870/)

## ESP32 as DMX receiver

* [Sparkfun –  Using Artnet DMX and the ESP32 to Drive Pixels](https://learn.sparkfun.com/tutorials/using-artnet-dmx-and-the-esp32-to-drive-pixels)

## Arduino as DMX receiver

* https://www.maxpierson.me/2009/04/29/arduino-dmx-512-io-shield/

# I have no idea what this is all about, but it looks promising

* <https://sites.google.com/site/rpidmx512/>
   * <https://sites.google.com/site/rpidmx512/raspberry-pi-rdm-controller>
   * <https://sites.google.com/site/rpidmx512/raspberry-pi-rdm-responder>
* <https://github.com/vanvught/rpidmx512>

# DMX lighting control software for Mac

* <https://zarino.co.uk/post/udmx-mac/> – uDMX command line utility
* <https://lightkeyapp.com/en/> – free as long as you need fewer than 24 channels

# Raspberry Pi as Wifi access point and client

* <https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md#internet-sharing>
* <https://lb.raspberrypi.org/forums/viewtopic.php?t=211542>
* <http://www.marrold.co.uk/2017/03/using-raspberry-pi-3-as-wifi-client-and.html>
* <https://raspberrypi.stackexchange.com/questions/67601/>

# MQTT

* <https://github.com/DoESLiverpool/somebody-should/wiki/MQTT-services>
