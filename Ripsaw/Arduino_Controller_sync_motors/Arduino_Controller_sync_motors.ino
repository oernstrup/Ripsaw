const int motorLeftPin = 9;
const int motorRightPin = 10;
const int led = 13;

void setup() {
  Serial.begin(9600);
  pinMode(motorLeftPin, OUTPUT);
  pinMode(motorRightPin, OUTPUT);
  pinMode(led, OUTPUT);
  Serial.println("=== Arduino Motor Control with Turning ===");
}

void loop() {
  digitalWrite(led, HIGH);

  Serial.println("Forward for 2 seconds...");
  sendRCToBoth(1800, 1800, 2000);  // Forward

  Serial.println("Forward for 10 seconds...");
  sendRCToBoth(2000, 2000, 10000);  // Forward

  Serial.println("Stop for 1 second...");
  sendRCToBoth(1500, 1500, 1000);  // Stop

  Serial.println("Turn LEFT for 2 seconds...");
  sendRCToBoth(1200, 1800, 2000);  // Left motor backward, right forward

  Serial.println("Stop for 1 second...");
  sendRCToBoth(1500, 1500, 1000);  // Stop

  Serial.println("Turn RIGHT for 2 seconds...");
  sendRCToBoth(1800, 1200, 2000);  // Left forward, right backward

  Serial.println("Stop for 1 second...");
  sendRCToBoth(1500, 1500, 1000);  // Stop

  Serial.println("Backward for 2 seconds...");
  sendRCToBoth(1200, 1200, 2000);  // Reverse

  Serial.println("Stop for 1 second...");
  sendRCToBoth(1500, 1500, 1000);  // Stop

  digitalWrite(led, LOW);

  Serial.println("Cycle complete. Waiting 3 seconds...\n");
  delay(3000); // pause before repeating
}

// Sends RC-style PWM signals to both motors with separate values
void sendRCToBoth(int pulseLeft, int pulseRight, int durationMs) {
  unsigned long startTime = millis();

  while (millis() - startTime < durationMs) {
    digitalWrite(motorLeftPin, HIGH);
    digitalWrite(motorRightPin, HIGH);
    delayMicroseconds(min(pulseLeft, pulseRight));

    // If pulses are different, stagger the off-timing
    if (pulseLeft > pulseRight) {
      digitalWrite(motorRightPin, LOW);
      delayMicroseconds(pulseLeft - pulseRight);
      digitalWrite(motorLeftPin, LOW);
    } else {
      digitalWrite(motorLeftPin, LOW);
      delayMicroseconds(pulseRight - pulseLeft);
      digitalWrite(motorRightPin, LOW);
    }

    delayMicroseconds(20000 - max(pulseLeft, pulseRight));

    // Debug output
    Serial.print("[PWM] Left: ");
    Serial.print(pulseLeft);
    Serial.print(" us | Right: ");
    Serial.print(pulseRight);
    Serial.print(" us | Elapsed: ");
    Serial.print(millis() - startTime);
    Serial.println(" ms");
  }
}
