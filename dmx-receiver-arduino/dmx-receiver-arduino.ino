#include <Rdm_Defines.h>
#include <Rdm_Uid.h>
#include <Conceptinetics.h>

// Number of channels to be monitored by the dmx_slave object,
// starting with the start address.
#define DMX_SLAVE_CHANNELS 5

DMX_Slave dmx_slave(DMX_SLAVE_CHANNELS);

void setup() {
    // Enable DMX slave interface and start recording DMX data.
    dmx_slave.enable();

    // Set start address to 1 (this is also the default setting).
    dmx_slave.setStartAddress(1);

    // Set led pin as output pin.
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    if ( dmx_slave.getChannelValue(1) > 127 ) {
        // Fast blink when we get a high value over DMX.
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
    } else {
        // Slow blink when we get a low value over DMX.
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(1900);
    }
}
