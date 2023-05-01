long randNumber;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9800);
  randomSeed(analogRead(0));
}

void loop() {
  // put your main code here, to run repeatedly:
  randNumber = random(50);
  Serial.println(randNumber);
}
