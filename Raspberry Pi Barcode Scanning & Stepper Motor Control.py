import csv
import zbar
import time
import serial
import smbus2
from smbus2 import SMBus
import RPi.GPIO as GPIO

# UART setup for ESP communication
uart = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)

# Setup for TOF sensor (VL53L1X)
I2C_BUS = 1  # I2C bus number
TOF_ADDRESS = 0x29  # Default I2C address for VL53L1X
bus = SMBus(I2C_BUS)

# Motor steps control (via ESP, using UART)
STEP_X = 0
STEP_Y = 1

# TOF sensor VL53L1X initialization (using the address 0x29)
def init_tof():
    # Initialize TOF sensor
    bus.write_byte_data(TOF_ADDRESS, 0x00, 0x01)  # Example command to start TOF
    # Check for sensor boot
    time.sleep(0.1)

def get_depth():
    # Function to read depth from TOF sensor (simplified)
    depth = bus.read_byte_data(TOF_ADDRESS, 0x0F)
    return depth

# Function to control stepper motors via UART
def move_motor(axis, steps):
    command = f"MOVE {axis} {steps}\n"
    uart.write(command.encode())

# Initialize barcode scanner
def scan_barcode():
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    
    # Assuming use of a camera here
    # Capture from Pi Camera (code for camera capture)
    
    # Mock barcode scanning output
    barcode_data = "ItemXYZ123"
    return barcode_data

# CSV writing function
def write_to_csv(item_name, depths):
    file_path = "/mnt/data/data.csv"
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        row = [item_name] + depths
        writer.writerow(row)

def main():
    # Initialize TOF sensor
    init_tof()
    
    # Set grid-like scanning parameters
    width_pack = 10  # cm
    height_pack = 5  # cm
    total_positions = 12
    
    while True:
        item_name = scan_barcode()  # Step 1: Scan the barcode
        
        # Step 2: Gather depth measurements from 12 positions
        depths = []
        for i in range(total_positions):
            depth = get_depth()  # Get depth from TOF sensor
            depths.append(depth)
            
            # Move the motors to the next scanning position
            if i % 4 == 0:
                move_motor(STEP_X, width_pack)  # Move X axis
            else:
                move_motor(STEP_Y, height_pack)  # Move Y axis
            
            time.sleep(0.1)  # Wait for motors to stabilize
        
        # Step 3: Append data to CSV
        write_to_csv(item_name, depths)
        
        # Optionally, break out of the loop or add logic to wait for the next scan

if __name__ == "__main__":
    main()
