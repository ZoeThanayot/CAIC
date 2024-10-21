#include <ESP8266WiFi.h>
#include <espnow.h>

// ESP-NOW peer MAC address ของ ESP2 ที่ควบคุม Stepper Motors
uint8_t esp2_address[] = {0xF0, 0x24, 0xF9, 0x45, 0xA4, 0x04};

void setup() {
  Serial.begin(115200);  // UART (for communication with Raspberry Pi)

  // Initialize Wi-Fi and ESP-NOW
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Add the peer (ESP2 for controlling stepper motors)
  esp_now_add_peer(esp2_address, ESP_NOW_ROLE_COMBO, 1, NULL, 0);
  
  Serial.println("System Initialized and ready to receive commands.");
}

void sendCommandToESP2(String command) {
  esp_now_send(esp2_address, (uint8_t *)command.c_str(), command.length());
}

void loop() {
  // Wait for incoming commands from Raspberry Pi
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    Serial.println("Command received: " + command);
    
    // Send the command to ESP2
    sendCommandToESP2(command);
    Serial.println("Command sent to ESP2: " + command);
  }
}
