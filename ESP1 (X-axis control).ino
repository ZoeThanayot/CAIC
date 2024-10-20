#include <ESP8266WiFi.h>
#include <espnow.h>
#include <Stepper.h>

// Stepper Motor Pins and Steps for X-axis
#define X_STEPS_PER_REV 200
Stepper x_stepper(X_STEPS_PER_REV, D1, D3, D2, D4);  // Example pin connections for the stepper motor

// ESP-NOW peer MAC address (of ESP2)
uint8_t esp2_address[] = {0x24, 0x6F, 0x28, 0xAE, 0x12, 0x34};

// UART settings for receiving commands from Raspberry Pi
void setup() {
  Serial.begin(115200);  // UART
  x_stepper.setSpeed(60); // RPM

  // Initialize Wi-Fi and ESP-NOW
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Add the peer (ESP2 for Y-axis)
  esp_now_add_peer(esp2_address, ESP_NOW_ROLE_COMBO, 1, NULL, 0);
}

void moveX(int steps) {
  x_stepper.step(steps);  // Move X-axis stepper
  delay(100);  // Delay to allow motor to finish movement
}

void sendToY() {
  // After X-axis movement, send a message to Y-axis ESP (ESP2)
  String message = "MOVE_Y";  // Example message
  esp_now_send(esp2_address, (uint8_t *)message.c_str(), message.length());
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    
    if (command.startsWith("MOVE X")) {
      int steps = command.substring(6).toInt();  // Extract number of steps
      moveX(steps);  // Move X-axis motor
      
      sendToY();  // Notify Y-axis ESP to move next
    }
  }
}
