long randNumber;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

void loop() {
  // put your main code here, to run repeatedly:
  randNumber = float(random(500))/10.0;
  Serial.println(randNumber);
}
