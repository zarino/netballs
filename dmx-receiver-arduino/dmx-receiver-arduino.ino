#include <Rdm_Defines.h>
#include <Rdm_Uid.h>
#include <Conceptinetics.h>

#include <SoftwareSerial.h>

// Number of channels to be monitored by the dmx_slave object,
// starting with the start address.
#define DMX_SLAVE_CHANNELS 5

// The first channel to monitor.
// As it happens, 1 is the default for .setStartAddress() anyway.
#define DMX_START_ADDRESS 1

// We're using Software Serial, because the normal serial pins
// and USB serial comms are being used by the DMX shield.
#define SERIAL_RX_PIN 10
#define SERIAL_TX_PIN 11
#define SERIAL_BAUD_RATE 9600

DMX_Slave dmx_slave(DMX_SLAVE_CHANNELS);

SoftwareSerial software_serial(SERIAL_RX_PIN, SERIAL_TX_PIN);

void setup() {
    // Enable DMX slave interface and start recording DMX data.
    dmx_slave.enable();

    dmx_slave.setStartAddress(DMX_START_ADDRESS);

    software_serial.begin(SERIAL_BAUD_RATE);
}

void loop() {
    // Send the values of the DMX channels, over serial, as space separated string.
    for (int i=DMX_START_ADDRESS; i<DMX_START_ADDRESS+DMX_SLAVE_CHANNELS; i++) {
        software_serial.print( dmx_slave.getChannelValue(i) );
        software_serial.print( ' ' );
    }
    software_serial.println();
}
