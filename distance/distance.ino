const int trigPin = 9;
const int echoPin = 10;

long duration;
float distanceCm;
float distanceInch;

void setup() {
  Serial.begin(9600);         // Start serial communication
  pinMode(trigPin, OUTPUT);   // Set trig pin as output
  pinMode(echoPin, INPUT);    // Set echo pin as input
}

void loop() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Trigger the sensor by sending a 10µs HIGH pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echoPin: time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Convert duration to distance
  distanceCm = duration * 0.0343 / 2;
  distanceInch = distanceCm / 2.54;

  // Print results
  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.print(" cm  |  ");
  Serial.print(distanceInch);
  Serial.println(" in");

  delay(500); // Wait before next reading
}

