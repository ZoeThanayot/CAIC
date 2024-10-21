#include <ESP8266WiFi.h>
#include <espnow.h>
#include <AccelStepper.h>

// Define pins for X and Y axes (STEP, DIR)
#define X_STEP_PIN 13
#define X_DIR_PIN 12
#define Y_STEP_PIN 14
#define Y_DIR_PIN 27

// Define stepper motors for X and Y axes
AccelStepper x_stepper(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
AccelStepper y_stepper(AccelStepper::DRIVER, Y_STEP_PIN, Y_DIR_PIN);

// Callback function to handle incoming ESP-NOW messages
void onReceive(uint8_t *mac, uint8_t *incomingData, uint8_t len) {
  String command = String((char*)incomingData).substring(0, len);
  Serial.println("Command received: " + command);

  // Check if the command is for moving the X-axis
  if (command.startsWith("MOVE X")) {
    int steps = command.substring(6).toInt();  // Extract number of steps for X-axis
    Serial.println("Moving X-axis: " + String(steps) + " steps");
    moveX(steps);  // Move X-axis motor
  }
  // Check if the command is for moving the Y-axis
  else if (command.startsWith("MOVE Y")) {
    int steps = command.substring(6).toInt();  // Extract number of steps for Y-axis
    Serial.println("Moving Y-axis: " + String(steps) + " steps");
    moveY(steps);  // Move Y-axis motor
  }
}

void moveX(int steps) {
  x_stepper.move(steps);  // Move X-axis motor
  while (x_stepper.distanceToGo() != 0) {
    x_stepper.run();  // Continue moving until target is reached
  }
}

void moveY(int steps) {
  y_stepper.move(steps);  // Move Y-axis motor
  while (y_stepper.distanceToGo() != 0) {
    y_stepper.run();  // Continue moving until target is reached
  }
}

void setup() {
  Serial.begin(115200);  // UART (for debug)

  // Set max speed and acceleration for X and Y motors
  x_stepper.setMaxSpeed(1000);  // Adjust as needed
  x_stepper.setAcceleration(500);  // Adjust as needed
  
  y_stepper.setMaxSpeed(1000);  // Adjust as needed
  y_stepper.setAcceleration(500);  // Adjust as needed

  // Initialize Wi-Fi and ESP-NOW
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Set callback function to handle received ESP-NOW messages
  esp_now_set_self_role(ESP_NOW_ROLE_COMBO);
  esp_now_register_recv_cb(onReceive);
  
  Serial.println("System Initialized and ready to control motors.");
}

void loop() {
  // No need for code in loop, since everything is handled via ESP-NOW callback
}
