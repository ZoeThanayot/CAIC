import csv
import time
import smbus2
import cv2
import zbarlight
from PIL import Image
import serial
import RPi.GPIO as GPIO

# Setup for I2C TOF Sensor
I2C_BUS = 1
VL53L1X_ADDRESS = 0x29
bus = smbus2.SMBus(I2C_BUS)

# UART Serial Communication with ESP
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# File to store data
csv_filename = "data.csv"

# Setup GPIO for motors if needed
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Stepper motor pins (if controlled from Pi) - example setup
STEP_X_PIN = 17
DIR_X_PIN = 27
STEP_Y_PIN = 22
DIR_Y_PIN = 23

# Set up GPIO pins for stepper control
GPIO.setup(STEP_X_PIN, GPIO.OUT)
GPIO.setup(DIR_X_PIN, GPIO.OUT)
GPIO.setup(STEP_Y_PIN, GPIO.OUT)
GPIO.setup(DIR_Y_PIN, GPIO.OUT)

# OpenCV Camera Setup
cap = cv2.VideoCapture(0)

def setup_tof_sensor():
    # Configuration for VL53L1X TOF sensor, optional if necessary
    pass

def read_tof_sensor():
    # Function to read depth data from TOF sensor
    # Replace this with actual TOF sensor reading logic
    return bus.read_byte_data(VL53L1X_ADDRESS, 0x01)  # Example

def move_stepper_motor(axis, steps, direction):
    # Function to send commands via UART to ESP or control motors locally
    # axis: "X" or "Y", steps: Number of steps, direction: 1 or -1
    if axis == "X":
        ser.write(f"MOVE X {steps} {direction}\n".encode())  # Send command to ESP
    elif axis == "Y":
        ser.write(f"MOVE Y {steps} {direction}\n".encode())  # Send command to ESP
    time.sleep(1)  # Wait for motor to finish moving

def scan_barcode():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert to grayscale for better barcode detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil_img = Image.fromarray(gray)
        barcodes = zbarlight.scan_codes('qrcode', pil_img)
        
        if barcodes:
            print(f"Barcode detected: {barcodes}")
            return barcodes[0]  # Return the first detected barcode
        
        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return None

def append_to_csv(item_name, depth_data):
    # Append the item name and depth data to CSV
    with open(csv_filename, mode='a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([item_name] + depth_data)

def main():
    print("Starting barcode scanning and depth measurement...")

    while True:
        # Step 1: Scan the barcode
        barcode = scan_barcode()
        if barcode:
            print(f"Barcode: {barcode}")
        
        # Step 2: Initialize depth data array for 12 points
        depth_data = []
        
        # Step 3: Loop through positions to get depth at each point
        for position in range(12):
            print(f"Measuring position {position+1}")
            
            # Move motors to next position (e.g., grid positions)
            move_stepper_motor("X", steps=100, direction=1)  # Adjust 'steps' based on pack width
            move_stepper_motor("Y", steps=50, direction=1)   # Adjust 'steps' based on pack height
            
            # Read depth data from TOF sensor
            depth = read_tof_sensor()
            print(f"Depth at position {position+1}: {depth} cm")
            depth_data.append(depth)
        
        # Step 4: Append data to CSV
        append_to_csv(barcode, depth_data)
        
        # Prompt user if they want to continue
        cont = input("Continue scanning next item? (y/n): ")
        if cont.lower() != 'y':
            break

    # Release camera resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
