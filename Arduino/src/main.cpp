#include <Arduino.h>
#include <DHT.h>
#include <DHT_U.h>
#include <HX711.h>

#define DHT22PIN 2
#define DHTTYPE DHT22
// HX711 circuit wiring
#define LOADCELL_DOUT_PIN 3 
#define LOADCELL_SCK_PIN 4  
#define calibration_factor -7050.0 
DHT dht(DHT22PIN, DHTTYPE);
HX711 scale; 

float humidity;
float temp; 
float weight; 

void setup() {
  Serial.begin(9600);
  dht.begin(); 
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
}

void loop() {
  delay(2000);
  temp = dht.readTemperature();
  humidity = dht.readHumidity();
  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print(" Celsius, Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print(scale.get_units(), 1); //scale.get_units() returns a float
  Serial.print(" kgs"); //You can change this to kg but you'll need to refactor the calibration_factor
  Serial.println();
}
