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

// We think there's some weird timing issue if you try to
// software_serial.print() inside the onReceiveComplete callback.
// So here we set up an array to batch up values, so we can print
// a bunch of them at once, outside the getChannelValue() loop.
uint8_t latestValues[DMX_SLAVE_CHANNELS];

void setup() {
    // Enable DMX slave interface and start recording DMX data.
    dmx_slave.enable();

    dmx_slave.setStartAddress(DMX_START_ADDRESS);

    // Tell DMX_Slave to call this callback when it receives a full frame.
    dmx_slave.onReceiveComplete(onFrameReceiveComplete);

    software_serial.begin(SERIAL_BAUD_RATE);
}

void loop() {
    for (int i=0; i<DMX_SLAVE_CHANNELS; i++) {
        software_serial.print( latestValues[i] );
        software_serial.print( " " );
    }
    software_serial.println();
    delay(50);
}

void onFrameReceiveComplete (unsigned short channelsReceived) {
    // Wait until we've been notified about a frame with all the required channels.
    if ( channelsReceived == DMX_SLAVE_CHANNELS) {
        // Store the current value of each channel, so the main loop()
        // can access the latest values when it comes time to print.
        for (int i=DMX_START_ADDRESS; i<DMX_START_ADDRESS+DMX_SLAVE_CHANNELS; i++) {
            latestValues[i-DMX_START_ADDRESS] = dmx_slave.getChannelValue(i);
        }
    }
}
