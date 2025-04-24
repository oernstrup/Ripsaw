

// Left motor signal pin
const int motorLeftPin = 9;  // PWM pin (e.g., D9)

// Right motor signal pin
const int motorRightPin = 10; // PWM pin (e.g., D10)

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;

void setup() {

  Serial.begin(9600);
  pinMode(motorLeftPin, OUTPUT);
  pinMode(motorRightPin, OUTPUT);
  
 //LED: Initialize the digital pin as an output.
  pinMode(led, OUTPUT);  
}

void loop() {
   Serial.println("Move both motors forward for 60 sec. ");
  // Move both motors forward for 60 sec. 
  for (int i = 0; i < 60; i++) { 
      Serial.print("i = ");
           Serial.println(i);
      sendRC(motorLeftPin, 1800);
      sendRC(motorRightPin, 1800);
    }

  // Move both motors forward
  Serial.println("Move both motors forward");
  sendRC(motorLeftPin, 1800);
  sendRC(motorRightPin, 1800);
  delay(2000);

  // Stop both motors
  Serial.println("Stop both motors ");
  sendRC(motorLeftPin, 1500);
  sendRC(motorRightPin, 1500);
  delay(1000);

  // Move backward
  Serial.println("Move backward ");
  sendRC(motorLeftPin, 1200);
  sendRC(motorRightPin, 1200);
  delay(2000);

  // Stop again
  Serial.println("Stop again ");
  sendRC(motorLeftPin, 1500);
  sendRC(motorRightPin, 1500);
  delay(1000);
}

// Simulate RC servo signal: 1ms to 2ms pulse every 20ms
void sendRC(int pin, int pulseWidthMicros) {

  Serial.print("Pin: ");
  Serial.print(pin);
  Serial.print(" pulseWidthMicros: ");
  Serial.println(pulseWidthMicros);

  for (int i = 0; i < 50; i++) { // send for ~1 second
    digitalWrite(pin, HIGH);
    delayMicroseconds(pulseWidthMicros);
    digitalWrite(pin, LOW);
    delay(20 - pulseWidthMicros / 1000); // wait until 20ms total
  }
}
