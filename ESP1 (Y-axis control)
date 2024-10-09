#include <esp_now.h>
#include <WiFi.h>
#include <AccelStepper.h>

#define stepPinY  12 // step pin 
#define dirPinY   14 // direction pin 

AccelStepper stepperY(AccelStepper::DRIVER, stepPinY, dirPinY);


uint8_t broadcastAddress[] = {0x24, 0x6F, 0x28, 0xAA, 0xBB, 0xCC}; // ใส่Mac ESPแกนXมานะจั้บพี่สุ่มใส่มั่วๆไปก่อน

typedef struct {
    int commandX; // ส่งข้อมูลแกนX
    int stepsX;
} struct_message;

struct_message myData;

void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    Serial.print("\nSend status: ");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Fail");
}

void setup() {
    Serial.begin(115200);
    // stepper set here na
    stepperY.setMaxSpeed(1000);
    stepperY.setAcceleration(500);
    WiFi.mode(WIFI_STA);
    // แค่เช็คESP-NOW 
    if (esp_now_init() != ESP_OK) {
        Serial.println("Error ESP-NOW");
        return;
    }
    esp_now_register_send_cb(onDataSent);
    // เพิ่มเป็น peer
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, broadcastAddress, 6);
    peerInfo.channel = 0;  
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("addไม่ได้ peer");
        return;
    }
}
void loop() {
    // อ่านUART inputจากRPI
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        int stepsY = input.toInt();
        Serial.println("Received Y steps: " + String(stepsY));
        stepperY.moveTo(stepsY);
        stepperY.runToPosition();

        // อันนี้ส่งแกนX
        myData.commandX = 1;  // ค้่าสมมุติปรับได้
        myData.stepsX = 500;  // ค้่าสมมุติปรับได้
        esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));

        if (result == ESP_OK) {
            Serial.println("ESP2ส่งได้");
        } else {
            Serial.println("Error ESP2");
        }
    }
}
