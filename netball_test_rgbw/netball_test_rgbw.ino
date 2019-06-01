// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN             6 // LED data pin
#define PUSHBUTTON_PIN  8

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 9 // Popular NeoPixel ring size

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRBW + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

byte colorTable[][4] = {
  { 255, 0  , 0  , 0   },    // red
  { 0  , 255, 0  , 0   },    // green
  { 0  , 0  , 255, 0   },    // blue
  { 255, 255, 0  , 0   },    // yellow
  { 255, 0,   255, 0   },    // magenta
  { 0  , 255, 255, 0   },    // cyan
  { 255, 255, 255, 0   },    // RGB white
  { 0  , 0  , 0  , 255 },    // Real white
  { 255, 255, 255, 255 }     // RGBW white
};

const int NUMBER_OF_COLORS = sizeof(colorTable) / 4;

void setup() {
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pinMode(PUSHBUTTON_PIN, INPUT_PULLUP);

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)

  whiteCompare();
}

int currentColor = 0;    // zero is the first color in the colorTable

void loop() {

  while(digitalRead(PUSHBUTTON_PIN) == HIGH)     // wait in this loop while no button pressed
    ;

  delay(50);                                     // debounce delay

  while(digitalRead(PUSHBUTTON_PIN) == LOW)      // wait for button to be released
    ;

  if(++currentColor == NUMBER_OF_COLORS)         // step through all colors in the colorTable
    currentColor = 0;

  displayEffects(currentColor);

  delay(50);                                     // debounce delay

}

void displayEffects(char col) {
  pixels.clear(); // Set all pixel colors to 'off'

  for (int i = 0; i < NUMPIXELS; i++) { // For each pixel...
    pixels.setPixelColor(i, pixels.Color(colorTable[col][0], colorTable[col][1], colorTable[col][2], colorTable[col][3]));
  }

  pixels.show();   // Send the updated pixel colors to the hardware.


}

// whiteCompare() - test function to compare white LEDs
void whiteCompare(void) {
  pixels.clear(); // Set all pixel colors to 'off'

  pixels.setPixelColor(0, pixels.Color(255, 255, 255, 0  ));   // RGB white
  pixels.setPixelColor(1, pixels.Color(255, 255, 255, 0  ));   // RGB white
  pixels.setPixelColor(2, pixels.Color(255, 255, 255, 0  ));   // RGB white

  pixels.setPixelColor(3, pixels.Color(0  , 0  , 0  , 255));   // Real white
  pixels.setPixelColor(4, pixels.Color(0  , 0  , 0  , 255));   // Real white
  pixels.setPixelColor(5, pixels.Color(0  , 0  , 0  , 255));   // Real white

  pixels.setPixelColor(6, pixels.Color(255, 255, 255, 255));   // RGBW white
  pixels.setPixelColor(7, pixels.Color(255, 255, 255, 255));   // RGBW white
  pixels.setPixelColor(8, pixels.Color(255, 255, 255, 255));   // RGBW white

  pixels.show();   // Send the updated pixel colors to the hardware.


}
