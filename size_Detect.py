import cv2 
import numpy as np 

# Initialize the webcam
cap = cv2.VideoCapture(1)  # Use 0 for the default camera

# Constants for size filtering (in centimeters)
MIN_SIZE = 0.0  # Minimum size to detect
MAX_SIZE = 200.0  # Maximum size to detect
PIXELS_PER_CM = 11.2  # Adjust this based on calibration <--------------------------------------- Edit!!!! from calibrate

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    # Apply a threshold to the frame to 
    # separate the objects from the background 
    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) 

    # Find the contours of the objects in the frame 
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    # Loop through the contours and calculate the area of each object 
    for cnt in contours: 
        area = cv2.contourArea(cnt) 

        # Calculate the bounding box and convert dimensions to centimeters
        x, y, w, h = cv2.boundingRect(cnt) 
        width_cm = w / PIXELS_PER_CM
        height_cm = h / PIXELS_PER_CM

        # Skip objects outside the specified size range
        if width_cm < MIN_SIZE or width_cm > MAX_SIZE or height_cm < MIN_SIZE or height_cm > MAX_SIZE:
            continue

        # Draw a bounding box around each 
        # object and display the dimensions on the frame 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) 
        cv2.putText(frame, f"{width_cm:.1f}x{height_cm:.1f} cm", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) 

    # Show the frame with the bounding boxes 
    # and dimensions of the objects overlaid on top 
    cv2.imshow('Real-Time Object Measurement', frame) 

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows() 

# Code By SR.Dhanush 
