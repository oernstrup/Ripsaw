const int motorLeftPin = 9;
const int motorRightPin = 10;
const int led = 13;

String inputString = "";
bool newCommand = false;

void setup() {
  Serial.begin(9600);
  pinMode(motorLeftPin, OUTPUT);
  pinMode(motorRightPin, OUTPUT);
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  Serial.println("=== Arduino Serial Motor Control Ready ===");
}

void loop() {
  // Collect characters from serial
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      newCommand = true;
    } else {
      inputString += inChar;
    }
  }

  if (newCommand) {
    Serial.print("inputString: ");
    Serial.println(inputString);
    processCommand(inputString);
    inputString = "";
    newCommand = false;
  }
}

// Converts speed (0-255) to PWM pulse width (us) for RC-style
int speedToPulse(int base, int speed) {
  // Clamp speed between 0–255
  Serial.print("[speedToPulse] Speed input: ");
  Serial.print(speed);
  
  speed = constrain(speed, -500, 500);
  Serial.print(" Speed out: ");
  Serial.println(speed);
  return base + speed; //map(speed, -500, 500, -100, 100);  // 1500us to 2000us or 1000us
}

// // Process command like F200, L150, etc.
// void processCommand(String cmd) {
//   if (cmd.length() < 2) return;

//   char dir = cmd.charAt(0);
//   int speed = cmd.substring(1).toInt();

//   Serial.print("[ProcessCommand] Dir: ");
//   Serial.print(dir);
//   Serial.print(" speed: ");
//   Serial.println(speed);

//    int leftPulse = 2100;
//    int rightPulse = 2100;

//   // digitalWrite(led, HIGH);
//   // sendRCToBoth(leftPulse, rightPulse, 1000); // 50 ms pulse burst
//   // digitalWrite(led, LOW);


// //  Serial.println("**** Forward ***"); 
// //  int leftPulse = 1600;
// //  int rightPulse = 1600;

//   //Serial.println("Left: " + String(leftPulse) + "Right: " + String(rightPulse));
//   //sendRCToBoth(leftPulse, rightPulse, 1000); // 50 ms pulse burst

// // delay(3000);

// // Serial.println("Forward +100 RPM");
// // sendRCToBoth(1400, 1400, 3000); 
// // delay(3000);

// // Serial.println("Stopping 0 RPM");
// // sendRCToBoth(2100, 2100, 3000); 
// // delay(3000);

// // Serial.println("Reverse (-100 RPM)");
// // sendRCToBoth(2900, 2900, 3000); 

// // delay(3000);



// }

void processCommand(String cmd) {
  if (cmd.length() < 2) return;

  char dir = cmd.charAt(0);
  int speed = cmd.substring(1).toInt();

  Serial.print("[ProcessCommand] Dir: ");
  Serial.print(dir);
  Serial.print(" speed: ");
  Serial.println(speed);

  int leftPulse = 2100;
  int rightPulse = 2100;

int median = 2100; 
 
  switch (dir) {
    case 'F':
      leftPulse = speedToPulse(median, -speed); // Inverted left
      rightPulse = speedToPulse(median, speed);
      Serial.println("[CMD] Forward");
      break;

    case 'B':
      leftPulse = speedToPulse(median, speed);  // Inverted left
      rightPulse = speedToPulse(median, -speed);
      Serial.println("[CMD] Backward");
      break;

    case 'L':
      leftPulse = speedToPulse(median, speed);  // Inverted left
      rightPulse = speedToPulse(median, speed);
      Serial.println("[CMD] Turn Left");
      break;

    case 'R':
      leftPulse = speedToPulse(median, -speed); // Inverted left
      rightPulse = speedToPulse(median, -speed);
      Serial.println("[CMD] Turn Right");
      break;

    case 'S':
      leftPulse = median;
      rightPulse = median;
      Serial.println("[CMD] Stop");
      break;

    default:
      Serial.println("[ERROR] Invalid direction");
      return;
  }

  digitalWrite(led, HIGH);
  sendRCToBoth(leftPulse, rightPulse, 1000); // 50 ms pulse burst
  digitalWrite(led, LOW);
}

// // Sends RC-style PWM to motors for a short duration
// void sendRCToBoth(int pulseLeft, int pulseRight, int durationMs) {
//   unsigned long startTime = millis();
//   while (millis() - startTime < durationMs) {
//     digitalWrite(motorLeftPin, HIGH);
//     digitalWrite(motorRightPin, HIGH);
//     delayMicroseconds(min(pulseLeft, pulseRight));

//     digitalWrite(motorRightPin, LOW);
//     digitalWrite(motorLeftPin, LOW);

//     // if (pulseLeft > pulseRight) {
//     //   digitalWrite(motorRightPin, LOW);
//     //   delayMicroseconds(pulseLeft - pulseRight);
//     //   digitalWrite(motorLeftPin, LOW);
//     // } else {
//     //   digitalWrite(motorLeftPin, LOW);
//     //   delayMicroseconds(pulseRight - pulseLeft);
//     //   digitalWrite(motorRightPin, LOW);
//     // }

//     delayMicroseconds(20000 - max(pulseLeft, pulseRight));
//   }

//   Serial.print("[PWM] L: ");
//   Serial.print(pulseLeft);
//   Serial.print(" | R: ");
//   Serial.print(pulseRight);
//   Serial.println(" (50ms burst)");
// }


void sendRCToBoth(int pulseLeft, int pulseRight, int durationMs) {
  unsigned long startTime = millis();
  while (millis() - startTime < durationMs) {
    unsigned long cycleStart = micros();

    digitalWrite(motorLeftPin, HIGH);
    digitalWrite(motorRightPin, HIGH);

    delayMicroseconds(min(pulseLeft, pulseRight));

    if (pulseLeft > pulseRight) {
      digitalWrite(motorRightPin, LOW);
      delayMicroseconds(pulseLeft - pulseRight);
      digitalWrite(motorLeftPin, LOW);
    } else {
      digitalWrite(motorLeftPin, LOW);
      delayMicroseconds(pulseRight - pulseLeft);
      digitalWrite(motorRightPin, LOW);
    }

    // Wait for rest of 20 ms frame
    unsigned long cycleTime = micros() - cycleStart;
    if (cycleTime < 20000) {
      delayMicroseconds(20000 - cycleTime);
    }
  }

  Serial.print("[PWM] L: ");
  Serial.print(pulseLeft);
  Serial.print(" | R: ");
  Serial.print(pulseRight);
  Serial.println(" (Accurate 50Hz burst)");
}