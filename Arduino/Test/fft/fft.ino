#include "arduinoFFT.h"

#define SAMPLES 512
#define SAMPLING_FREQUENCY 2048

arduinoFFT FFT = arduinoFFT();

unsigned int samplingPeriod;
unsigned long microSeconds;

double vReal[SAMPLES]; // create vector of size SAMPLES to hold real values
double vImag[SAMPLES]; // create vector of size SAMPLES to hold imaginary values

void setup() {
  Serial.begin(115200); // Baud rate for the Serial Monitor
  samplingPeriod = round(1000000 * (1.0 / SAMPLING_FREQUENCY)); // period in microseconds
}

void loop() {
  // Sample SAMPLES times
  for (int i = 0; i < SAMPLES; i++) {
    microSeconds = micros(); // returns the number of microseconds since the Arduino board began running the current script

    vReal[i] = analogRead(34); // reads the value from the analog pin 0 (A0), quantize it and save it as a real term
    vImag[i] = 0; // makes imaginary term 0 always

    // remaining wait time between samples if necessary
    while (micros() < (microSeconds + samplingPeriod)) {
      // do nothing
    }
  }

  // perform FFT on samples
  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);

  // find peak frequency and print peak
  double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
  Serial.println(peak); // print out the most dominant frequency

  // Add a delay to control the loop frequency
  delay(1000); // Adjust the delay time as needed
}
