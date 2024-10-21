#include <esp_now.h>
#include <WiFi.h>

// Define UART pins for communication with Raspberry Pi
#define RX_PIN 16
#define TX_PIN 17

// Structure to hold motor commands (steps and direction)
typedef struct struct_message {
    int motor1_steps;     // Number of steps for motor 1
    int motor1_dir;       // Direction for motor 1 (0 or 1)
    int motor2_steps;     // Number of steps for motor 2
    int motor2_dir;       // Direction for motor 2 (0 or 1)
} struct_message;

struct_message motor_data;
uint8_t receiverMacAddress[] = {0xF0, 0x24, 0xF9, 0x45, 0xA4, 0x04}; // Receiver ESP32 MAC address

void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN); // UART for Raspberry Pi

    // Indicate that the code has started running
    Serial.println("Code uploaded successfully! Starting up...");

    // Initialize ESP-NOW
    WiFi.mode(WIFI_STA);
    if (esp_now_init() != ESP_OK) {
        Serial.println("Error initializing ESP-NOW");
        return;
    }
  
    // Add peer (receiver)
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, receiverMacAddress, 6);
    peerInfo.channel = 0;  
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("Failed to add peer");
        return;
    }

    // Indicate successful setup
    Serial.println("ESP-NOW initialized and peer added successfully.");
}

void loop() {
    // Read UART data from Raspberry Pi
    if (Serial2.available() > 0) {
        String input = Serial2.readStringUntil('\n');
        parseInput(input); // Function to parse the input into motor steps and direction

        // Send motor control data via ESP-NOW
        esp_err_t result = esp_now_send(receiverMacAddress, (uint8_t *) &motor_data, sizeof(motor_data));
        
        if (result == ESP_OK) {
            Serial.println("Data sent to receiver");
        } else {
            Serial.println("Error sending data");
        }
    }
}

// Function to parse UART input (example format "100,0,200,1" for motor1 and motor2 steps/directions)
// Format: motor1_steps,motor1_dir,motor2_steps,motor2_dir
void parseInput(String input) {
    int commaIndex1 = input.indexOf(',');
    int commaIndex2 = input.indexOf(',', commaIndex1 + 1);
    int commaIndex3 = input.indexOf(',', commaIndex2 + 1);

    motor_data.motor1_steps = input.substring(0, commaIndex1).toInt();
    motor_data.motor1_dir = input.substring(commaIndex1 + 1, commaIndex2).toInt();
    motor_data.motor2_steps = input.substring(commaIndex2 + 1, commaIndex3).toInt();
    motor_data.motor2_dir = input.substring(commaIndex3 + 1).toInt();
}
