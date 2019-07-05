#include <SoftwareSerial.h>

// We're using Software Serial, because the normal serial pins
// and USB serial comms are being used by the DMX shield.
#define SERIAL_RX_PIN 10
#define SERIAL_TX_PIN 11
#define SERIAL_BAUD_RATE 9600

SoftwareSerial software_serial(SERIAL_RX_PIN, SERIAL_TX_PIN);

void setup() {
    software_serial.begin(SERIAL_BAUD_RATE);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    software_serial.print("255 255 255 255 255 ");
    software_serial.println();

    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(400);
}
