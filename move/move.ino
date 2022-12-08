#include "Keyboard.h"

void setup() {
  Serial.begin(9600);
  Keyboard.begin();
}

void loop() {
  if (Serial.available() > 0) {
    switch (Serial.read()) {
      case 'r':
        Keyboard.write(KEY_RIGHT_ARROW);
        break;
      case 'l':
        Keyboard.write(KEY_LEFT_ARROW);
        break;
      case 'u':
        Keyboard.write(KEY_UP_ARROW);
        break;
      case 'd':
        Keyboard.write(KEY_DOWN_ARROW);
        break;
      case 's':
        Keyboard.press(KEY_LEFT_SHIFT);
        delay(100);
        Keyboard.release(KEY_LEFT_SHIFT);
        break;
      case 'w':
        delay(100);
        break;
    }
  }
}