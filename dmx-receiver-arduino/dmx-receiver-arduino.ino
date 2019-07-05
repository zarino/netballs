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
#define BATCH_SIZE 20
uint8_t valuesToPrint[BATCH_SIZE];
uint8_t valuesStored = 0;

void setup() {
    // Enable DMX slave interface and start recording DMX data.
    dmx_slave.enable();

    dmx_slave.setStartAddress(DMX_START_ADDRESS);

    // Tell DMX_Slave to call this callback when it receives a full frame.
    dmx_slave.onReceiveComplete(onFrameReceiveComplete);

    software_serial.begin(SERIAL_BAUD_RATE);
}

void loop() {

}

void onFrameReceiveComplete (unsigned short channelsReceived) {
    if ( channelsReceived == DMX_SLAVE_CHANNELS) {

        for (int i=DMX_START_ADDRESS; i<DMX_START_ADDRESS+DMX_SLAVE_CHANNELS; i++) {
            valuesToPrint[valuesStored] = dmx_slave.getChannelValue(i);
            valuesStored++;
        }

        if (valuesStored == BATCH_SIZE) {

            int8_t index = 0;
            for (int row=0; row<(BATCH_SIZE / DMX_SLAVE_CHANNELS); row++) {
                for (int j=0; j<DMX_SLAVE_CHANNELS; j++) {
                    software_serial.print( valuesToPrint[ index++] );
                    software_serial.print( " " );
                }
                software_serial.println();
            }

            valuesStored = 0;
        }

    }
}
