import RPi.GPIO as GPIO
from time import sleep
import serial
import zbarlight
from picamera import PiCamera
from PIL import Image

# Setup for stepper motor
DIR = 20
STEP = 21
CW = 1
CCW = 0
SPR = 200
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# UART communication setup
ser = serial.Serial('/dev/ttyS0', 9600)

# Camera setup
camera = PiCamera()

# Function to scan barcode
def scan_barcode():
    camera.capture('barcode.jpg')
    with open('barcode.jpg', 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
        codes = zbarlight.scan_codes('ean13', image)
        if codes:
            return codes[0].decode('utf-8')
        return None

# Function to control stepper motor
def move_motor(direction, steps):
    GPIO.output(DIR, direction)
    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.005)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.005)

# Main operation loop
try:
    while True:
        barcode = scan_barcode()
        if barcode:
            print(f"Barcode: {barcode}")
            # Control stepper motor (move in grid-like pattern)
            move_motor(CW, SPR * 2)
            move_motor(CCW, SPR * 2)
            
            # Send barcode data via UART
            data = f"{barcode},X:10,Y:20\n"
            ser.write(data.encode())
            sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
    ser.close()
