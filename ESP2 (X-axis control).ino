#include <esp_now.h>
#include <WiFi.h>
#include <AccelStepper.h>

#define stepPinX  26 // Set step pin
#define dirPinX   27 // Set direction

AccelStepper stepperX(AccelStepper::DRIVER, stepPinX, dirPinX);

typedef struct {
    int commandX;
    int stepsX;
} struct_message;

struct_message incomingData;

void onDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
    memcpy(&incomingData, incomingData, sizeof(incomingData));
    Serial.print("Steps X-axis: ");
    Serial.println(incomingData.stepsX);
    stepperX.moveTo(incomingData.stepsX);
    stepperX.runToPosition();
}

void setup() {
    Serial.begin(115200);
    stepperX.setMaxSpeed(1000);
    stepperX.setAcceleration(500);
    WiFi.mode(WIFI_STA);

    // เช้ค ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("ไม่มีESP-NOW");
        return;
    }
    esp_now_register_recv_cb(onDataRecv);
}

void loop() {
    stepperX.run();
}
