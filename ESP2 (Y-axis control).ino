#include <ESP8266WiFi.h>
#include <espnow.h>
#include <Stepper.h>

// Stepper Motor Pins and Steps for Y-axis
#define Y_STEPS_PER_REV 200
Stepper y_stepper(Y_STEPS_PER_REV, D1, D3, D2, D4);  // Example pin connections for the stepper motor

// Callback function to handle incoming ESP-NOW messages
void onReceive(uint8_t *mac, uint8_t *incomingData, uint8_t len) {
  String message = String((char*)incomingData).substring(0, len);
  
  if (message == "MOVE_Y") {
    moveY(100);  // Example: Move Y-axis stepper 100 steps (adjust as needed)
  }
}

void moveY(int steps) {
  y_stepper.step(steps);  // Move Y-axis motor
  delay(100);  // Delay to allow motor to finish movement
}

void setup() {
  Serial.begin(115200);  // UART (for debug)

  y_stepper.setSpeed(60); // RPM

  // Initialize Wi-Fi and ESP-NOW
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Set callback function to handle received ESP-NOW messages
  esp_now_set_self_role(ESP_NOW_ROLE_COMBO);
  esp_now_register_recv_cb(onReceive);
}

void loop() {
  // Nothing in the loop since we wait for commands via ESP-NOW
}
