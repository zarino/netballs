int dipPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
int dipPinsCount = 8;
int dmxAddress;

void setup() {
    Serial.begin(9600);

    for (int p=0; p<dipPinsCount; p++) {
        pinMode(dipPins[p], INPUT_PULLUP);
    }
}

void loop() {
    dmxAddress = 0;

    for (int p=0; p<dipPinsCount; p++) {
        int value = pinValue( dipPins[p] );
        dmxAddress = dmxAddress + (value << p);
    }

    Serial.println(dmxAddress);
}

int pinValue(int pin) {
    int val = digitalRead(pin);
    if ( val == HIGH ) {
        return 0;
    } else {
        return 1;
    }
}
