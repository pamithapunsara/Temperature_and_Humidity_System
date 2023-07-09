#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define LED_PIN_1 13  // GPIO pin D7 on NodeMCU
#define LED_PIN_2 12  

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LED_PIN_1, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);   // Set LED pin as output
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (!isnan(temperature) && !isnan(humidity)) {
    Serial.print(temperature);
    Serial.print(",");
    Serial.println(humidity);

    if (temperature > 26.5) {
      digitalWrite(LED_PIN_1, HIGH);  // Turn on the LED
    } else {
      digitalWrite(LED_PIN_1, LOW);  // Turn off the LED
    }
  }

  delay(1500);
   if (Serial.available()) {
    char command = Serial.read();
    if (command == 'H') {
      digitalWrite(LED_PIN_2, HIGH);
    } else if (command == 'L') {
      digitalWrite(LED_PIN_2, LOW);
    }
  }
}
