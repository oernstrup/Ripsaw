#include <uStepperS.h>

// RC-style PWM input pin (D2)
#define RC_PIN 2  

uStepperS stepper;

void setup() {
  Serial.begin(115200);
  while (!Serial);  // Wait for Serial monitor to open (optional, for debugging)
  
  stepper.setup();
  pinMode(RC_PIN, INPUT);

  Serial.println("\n=== uStepper RC Control Initialized ===");
  Serial.println("Waiting for RC signal on pin D2...");
}

void loop() {
  // Read RC pulse width in microseconds
  unsigned long pulseWidth = pulseIn(RC_PIN, HIGH, 25000); // 25ms timeout

  if (pulseWidth >= 1000 && pulseWidth <= 2000) {
    // Map 1000–2000 us pulse to -100 to 100 RPM
    float speed = map(pulseWidth, 1000, 2000, -500, 500); //Original +-100

    // Send speed to motor
    stepper.setRPM(speed);

    // Debug: Print incoming pulse and command
    Serial.print("[RC INPUT] Pulse: ");
    Serial.print(pulseWidth);
    Serial.print(" us => Speed command: ");
    Serial.print(speed);
    Serial.println(" RPM");
  } else {
    // Stop motor if pulse is out of expected range
    
    stepper.setRPM(0);

    // Debug: Notify invalid signal
    Serial.print("[RC INPUT] Invalid pulse: ");
    Serial.print(pulseWidth);
    Serial.println(" us. Motor stopped.");
  }

  delay(50); // Reduce spam and add some stability
}
