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
  return base + speed; //map(speed, -500, 500, -500, 500);  // 1500us to 2000us or 1000us
}

// Process command like F200, L150, etc.
void processCommand(String cmd) {
  if (cmd.length() < 2) return;

  char dir = cmd.charAt(0);
  int speed = cmd.substring(1).toInt();

  Serial.print("[ProcessCommand] Dir: ");
  Serial.print(dir);
  Serial.print(" speed: ");
  Serial.println(speed);

  int leftPulse = 1500;
  int rightPulse = 1500;

 
  switch (dir) {
    case 'F':
      leftPulse = speedToPulse(1500, -speed); // Inverted left
      rightPulse = speedToPulse(1500, speed);
      Serial.println("[CMD] Forward");
      break;

    case 'B':
      leftPulse = speedToPulse(1500, speed);  // Inverted left
      rightPulse = speedToPulse(1500, -speed);
      Serial.println("[CMD] Backward");
      break;

    case 'L':
      leftPulse = speedToPulse(1500, speed);  // Inverted left
      rightPulse = speedToPulse(1500, speed);
      Serial.println("[CMD] Turn Left");
      break;

    case 'R':
      leftPulse = speedToPulse(1500, -speed); // Inverted left
      rightPulse = speedToPulse(1500, -speed);
      Serial.println("[CMD] Turn Right");
      break;

    case 'S':
      leftPulse = 1500;
      rightPulse = 1500;
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

// Sends RC-style PWM to motors for a short duration
void sendRCToBoth(int pulseLeft, int pulseRight, int durationMs) {
  unsigned long startTime = millis();
  while (millis() - startTime < durationMs) {
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

    delayMicroseconds(20000 - max(pulseLeft, pulseRight));
  }

  Serial.print("[PWM] L: ");
  Serial.print(pulseLeft);
  Serial.print(" | R: ");
  Serial.print(pulseRight);
  Serial.println(" (50ms burst)");
}
