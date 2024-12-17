import cv2
import numpy as np
import math
from adafruit_servokit import ServoKit 
import board
import time  # Import time module for sleep functionality
from Guy_Calibration_PixelperCM import calibrate_pixels_per_cm
from Guy_Detect import detect
from Guy_calculate_test import Calculattion
from Guy_Servo import ControlServo

def main():
    try:
        # Step 1: Calibration
        print('Do you need to Calibrate?')
        calibrate_option = input('Y/N: ').strip().upper()
        
        if calibrate_option == 'Y':
            print("Starting Calibration...")
            calibrate_pixels_per_cm()
            print("Calibration complete!")
        elif calibrate_option == 'N':
            print("Skipping Calibration.")
        else:
            print("Invalid input! Exiting.")
            return
        
        # Step 2: Detection
        print('Do you need to Detect OG and OJ?')
        detect_option = input('Y/N: ').strip().upper()
        
        if detect_option == 'Y':
            print("Starting Object Detection...")
            detect()
            print("Object Detection complete!")
        elif detect_option == 'N':
            print("Skipping Detection.")
        else:
            print("Invalid input! Exiting.")
            return
        
        # Step 3: Calculation
        print('Do you need to perform Calculations?')
        calc_option = input('Y/N: ').strip().upper()
        
        if calc_option == 'Y':
            print("Starting Calculations...")
            Calculattion()
            print("Calculations complete!")
        elif calc_option == 'N':
            print("Skipping Calculations.")
        else:
            print("Invalid input! Exiting.")
            return
        
        # Step 4: Servo Control
        print('Do you need to Control the Servo?')
        servo_option = input('Y/N: ').strip().upper()
        
        if servo_option == 'Y':
            print("Starting Servo Control...")
            ControlServo()
            print("Servo Control complete!")
        elif servo_option == 'N':
            print("Skipping Servo Control.")
        else:
            print("Invalid input! Exiting.")
            return
        
        print("All processes done successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
