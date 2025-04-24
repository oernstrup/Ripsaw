const int sensorPin = A0;  // KY-018 signal pin connected to A0

void setup() {
  Serial.begin(9600);
}

void loop() {
  int lightLevel = analogRead(sensorPin);  // 0 - 1023
  Serial.print("Light Level(0 = dark, 1023 = Bright): ");
  Serial.println(lightLevel);
  delay(500);  // Read every half second
}

