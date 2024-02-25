const int sampleWindow = 50;  // Sample window width in mS (50 mS = 20Hz)
int const AMP_PIN = 34;       // Preamp output pin connected to A0
unsigned int sample;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  unsigned long startMillis = millis(); // Start of sample window
  unsigned int peakToPeak = 0;   // peak-to-peak level

  unsigned int signalMax = 0;
  unsigned int signalMin = 1024;

  // Collect data for 50 mS and then plot data
  while (millis() - startMillis < sampleWindow)
  {
    sample = analogRead(AMP_PIN);
    if (sample < 1024)  // Toss out spurious readings
    {
      if (sample > signalMax)
      {
        signalMax = sample;  // Save just the max levels
      }
      else if (sample < signalMin)
      {
        signalMin = sample;  // Save just the min levels
      }
    }
  }
  peakToPeak = signalMax - signalMin;  // Max - Min = peak-peak amplitude
  Serial.println(peakToPeak);
  delay(5000);
}
