/*
  Rui Santos
  Complete project details at our blog: https://RandomNerdTutorials.com/esp32-data-logging-firebase-realtime-database/
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files.
  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "arduinoFFT.h"

#include "time.h"

// Provide the token generation process info.
#include "addons/TokenHelper.h"
// Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "Galaxy M10298D"
#define WIFI_PASSWORD "ziyo4459"

// Insert Firebase project API Key
#define API_KEY "AIzaSyBScNMo0woCdn3TKGupwVgoC5Ii5bmn9rU"

// Insert Authorized Email and Corresponding Password
#define USER_EMAIL "nisal.saranga1234@gmail.com"
#define USER_PASSWORD "NSLlost123#"

// Insert RTDB URLefine the RTDB URL
#define DATABASE_URL "https://bees-9478f-default-rtdb.asia-southeast1.firebasedatabase.app/"

// Define Firebase objects
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// Variable to save USER UID
String uid;

// Database main path (to be updated in setup with the user UID)
String databasePath;
// Database child nodes
String tempPath = "/temperature";
String humPath = "/humidity";
String freqPath = "/frequency"; // Corrected variable name
String rainPath = "/rainfall";
String timePath = "/timestamp";


// Parent Node (to be updated in every loop)
String parentPath;

int timestamp;
FirebaseJson json;

const char* ntpServer = "pool.ntp.org";

// BME280 sensor

float temperature;
float humidity;
float frequency;
int rainfall;

// Timer variables (send new readings every three minutes)
unsigned long sendDataPrevMillis = 0;
unsigned long timerDelay = 180000;

#define SAMPLES 512
#define SAMPLING_FREQUENCY 2048

arduinoFFT FFT = arduinoFFT();

unsigned int samplingPeriod;
unsigned long microSeconds;

double vReal[SAMPLES]; // create vector of size SAMPLES to hold real values
double vImag[SAMPLES]; // create vector of size SAMPLES to hold imaginary values


// Initialize WiFi
void initWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
  Serial.println();
}

// Function that gets current epoch time
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

const int potpin = 35;
int potVal =0;

void setup(){
  Serial.begin(115200);
  samplingPeriod = round(1000000 * (1.0 / SAMPLING_FREQUENCY)); // period in microseconds


  initWiFi();
  configTime(0, 0, ntpServer);

  // Assign the api key (required)
  config.api_key = API_KEY;

  // Assign the user sign in credentials
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  // Assign the RTDB URL (required)
  config.database_url = DATABASE_URL;

  Firebase.reconnectWiFi(true);
  fbdo.setResponseSize(4096);

  // Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  // Assign the maximum retry of token generation
  config.max_token_generation_retry = 5;

  // Initialize the library with the Firebase authen and config
  Firebase.begin(&config, &auth);

  // Getting the user UID might take a few seconds
  Serial.println("Getting User UID");
  while ((auth.token.uid) == "") {
    Serial.print('.');
    delay(1000);
  }
  // Print user UID
  uid = auth.token.uid.c_str();
  Serial.print("User UID: ");
  Serial.println(uid);

  // Update database path
  databasePath = "/UsersData/" + uid + "/readings";
}

void loop(){
  for (int i = 0; i < SAMPLES; i++) {
    microSeconds = micros();

    vReal[i] = analogRead(34);
    vImag[i] = 0;

    while (micros() < (microSeconds + samplingPeriod)) {
      // do nothing
    }
  }

  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);

  frequency = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
  
  // You need to replace these with your actual functions or sensors
  // temperature = readTemperature();
  // humidity = readHumidity();

  // Example values (replace with actual readings)
  temperature = 25.5;
  humidity = 60.0;

  potVal = analogRead(potpin);
  rainfall = map(potVal, 0, 4095, 100, 0);

  if (Firebase.ready() && (millis() - sendDataPrevMillis > timerDelay || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();

    // Get current timestamp
    timestamp = getTime();
    Serial.print("time: ");
    Serial.println(timestamp);

    parentPath = databasePath + "/" + String(timestamp);

    // Clear the JSON object before setting new values
    json.clear();

    // Set values in the JSON
    json.set(tempPath.c_str(), String(temperature));
    json.set(humPath.c_str(), String(humidity));
    json.set(freqPath.c_str(), String(frequency)); // Corrected variable name
    json.set(rainPath.c_str(), String(rainfall));
    json.set(timePath.c_str(), String(timestamp));

    // Print the JSON string representation
    String jsonString;
    json.toString(jsonString);
    Serial.print("JSON Data: ");
    Serial.println(jsonString);

    // Send the JSON data to the database
    Serial.printf("Set json... %s\n", Firebase.RTDB.setJSON(&fbdo, parentPath.c_str(), &json) ? "ok" : fbdo.errorReason().c_str());
  }
}