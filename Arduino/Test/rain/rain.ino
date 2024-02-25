const int potpin = 35;
int potVal =0;

void setup()
{
  Serial.begin(115200);
  delay(1000);
}

void loop()
{
  potVal = analogRead(potpin);
  // Map the analog value to a range of 0 to 100
  int mappedValue = map(potVal, 0, 4095, 100, 0); // ESP32 has a 12-bit ADC, so the range is 0-4095

  // Print the mapped value to the serial monitor
  Serial.println(mappedValue);
  Serial.println(potVal);
  delay(500);
}
