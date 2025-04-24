const int trigPin = 9;
const int echoPin = 10;
const int sensorPin = A0;

void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT);  // LED pin
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  if (Serial.available()) {
    String msg = Serial.readString();
    int light = readLightLevel(); 

    Serial.print("Received: ");
    Serial.print(msg);
    Serial.print(" Distance: ");
    Serial.print(getDistanceCm(), 2);
    Serial.print(" cm.");
    Serial.print(" Light Level: ");
    Serial.println(light);


    digitalWrite(12, HIGH); // LED ON

    int var = 0;
    while (var < 10) {
      Blink(500);
      var++;
    }
  }
}

void Blink(int x) {
  digitalWrite(12, HIGH);
  delay(x);
  digitalWrite(12, LOW);
  delay(x);
}

float getDistanceCm() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float distanceCm = duration * 0.0343 / 2;

  return distanceCm;
}

// Function to read light level from KY-018
int readLightLevel() {
  return analogRead(sensorPin);  // Returns value from 0 (dark) to 1023 (bright)
}
