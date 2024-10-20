# **Automated Barcode Scanning & Depth Measurement System**

This project implements a barcode scanning and depth measurement system using a **Raspberry Pi 3**, **Zbar**, **VL53L1X TOF sensor**, **ESP8266 (or ESP32) controllers**, and **stepper motors**. The system scans barcodes, moves stepper motors to specified positions, collects depth data, and logs the results in a CSV file.

## **Project Structure**

- **Raspberry Pi (main controller)**:
  - Scans barcodes using Zbar.
  - Sends movement commands to the X-axis ESP via UART.
  - Reads depth data using a VL53L1X sensor.
  - Logs data (item name + depth values) to a CSV file.

- **ESP1 (X-axis)**:
  - Controls the X-axis stepper motor.
  - Communicates with ESP2 via ESP-NOW for Y-axis movement.

- **ESP2 (Y-axis)**:
  - Controls the Y-axis stepper motor.
  - Receives ESP-NOW messages from ESP1 to coordinate movements.

---

## **Hardware Requirements**

- **Raspberry Pi 3** (or any compatible version)
- **VL53L1X TOF sensor** (for depth measurement)
- **2x ESP8266/ESP32 boards** (for X and Y stepper motor control)
- **Stepper motors** (SONCOR Motor SC12STH47 or compatible)
- **Zbar library** for barcode scanning
- **UART communication** between Raspberry Pi and ESP1
- **ESP-NOW communication** between ESP1 and ESP2
- **Camera** (if needed for barcode scanning)

---

## **Software Requirements**

- **Raspberry Pi**:
  - Raspbian OS (or equivalent)
  - Python 3
  - Zbar for barcode scanning
  - `smbus2` for I2C communication with the TOF sensor
  - `RPi.GPIO` for general GPIO handling

- **ESP1 & ESP2**:
  - ESP8266 or ESP32 core (for Arduino IDE)
  - ESP-NOW library for wireless communication
  - Stepper library for motor control

---

## **Installation Instructions**

### **1. Set up Raspberry Pi**

1. **Install necessary libraries**:
   ```bash
   sudo apt-get update
   sudo apt-get install zbar-tools python3-zbar python3-smbus
   pip3 install smbus2 RPi.GPIO
   ```

2. **Enable I2C on Raspberry Pi**:
   ```bash
   sudo raspi-config
   ```
   - Navigate to **Interfacing Options > I2C > Enable**.

3. **Clone this repository**:
   ```bash
   git clone https://github.com/Jinwoo290350/CAIC.git
   cd CAIC
   ```

### **2. Set up ESPs (X and Y axis controllers)**

1. **Install the ESP8266/ESP32 core** on your Arduino IDE. Follow instructions [here](https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/) or [here](https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/).
   
2. **Upload the appropriate code** to each ESP:
   - **ESP1** (X-axis): Flash the code located in `ESP_X_AXIS.ino`.
   - **ESP2** (Y-axis): Flash the code located in `ESP_Y_AXIS.ino`.

### **3. Wiring Setup**

- **Raspberry Pi**:
  - Connect the **TOF sensor (VL53L1X)** via I2C (SDA to GPIO 2, SCL to GPIO 3).
  - UART connection to **ESP1** (TX and RX).
  
- **ESP1** (X-axis):
  - Connect stepper motor to the designated pins.
  - UART pins connected to Raspberry Pi.

- **ESP2** (Y-axis):
  - Connect stepper motor to the designated pins.
  - Communicates with ESP1 via ESP-NOW.

---

## **Running the System**

### **Raspberry Pi**

1. **Run the Python code**:
   ```bash
   python3 barcode_depth_control.py
   ```
   This will:
   - Scan a barcode.
   - Control the stepper motors (X and Y axes) through the ESP boards.
   - Collect depth data from the TOF sensor.
   - Append the collected data (Item Name + Depth values) to the CSV file.

2. **CSV Output**:
   - The CSV file `data.csv` will store each barcode’s item name and the corresponding depth measurements from 12 positions.

### **ESP Boards**

- **ESP1** (X-axis):
  - Receives UART commands from the Raspberry Pi.
  - Controls X-axis stepper motor and communicates with ESP2 to trigger Y-axis movement.

- **ESP2** (Y-axis):
  - Receives ESP-NOW commands from ESP1.
  - Controls Y-axis stepper motor based on the command received.

---

## **CSV File Format**

The CSV file will have the following structure:

| Item Name   | Depth Position 1 | Depth Position 2 | ... | Depth Position 12 |
|-------------|------------------|------------------|-----|-------------------|
| Barcode 001 | Depth 1 (cm)      | Depth 2 (cm)      | ... | Depth 12 (cm)      |
| Barcode 002 | Depth 1 (cm)      | Depth 2 (cm)      | ... | Depth 12 (cm)      |
| ...         | ...               | ...               | ... | ...               |

Each new scan will append a new row to the file.

---

## **Future Improvements**

- Add error handling for sensor failures.
- Implement real-time data visualization of depth measurements.
- Integrate multiple barcode formats for scanning flexibility.
  
---

## **Contributors**

- **Your Name** – Developer and Hardware Integrator
- **Contributors** – (List contributors if any)

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
