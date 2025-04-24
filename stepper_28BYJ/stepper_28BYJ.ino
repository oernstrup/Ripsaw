#include <Stepper.h>


//IN1	3
//IN2	4
//IN3	5
//IN4	6
//GND	GND
//VCC	5V (Rød på wall batteri)


// Define steps per revolution (for 28BYJ-48 it's usually 2048)
const int stepsPerRevolution = 2048;

// Connect IN1-IN4 to pins 8-11 on Arduino
Stepper myStepper(stepsPerRevolution, 4,6,5,7); // 8,10,9,11 --> 4,6,5,7
// Note: 2nd and 3rd pins are swapped due to motor sequence

void setup() {
  myStepper.setSpeed(10);  // Speed in RPM (Use setSpeed(5-15) for smoother movement. Going too fast can cause missed steps.) 10 = best
  Serial.begin(9600);
  Serial.println("Stepper motor ready.");
}

void loop() {
  Serial.println("Rotating one revolution clockwise...");
  myStepper.step(stepsPerRevolution);  // One full revolution clockwise
  delay(5000);

  Serial.println("Rotating one revolution counterclockwise...");
  myStepper.step(-stepsPerRevolution); // One full revolution counter-clockwise
  delay(5000);
}

