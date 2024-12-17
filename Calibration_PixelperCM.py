import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(1)  # Use 0 for the default camera

def calibrate_pixels_per_cm():
    print("Please place a reference object of known width in front of the camera.")
    ref_width_cm = float(input("Enter the width of the reference object in cm: "))

    while True:
        # Capture a frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale and detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        # Find contours
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 100:  # Ignore small contours
                continue

            # Get the bounding box of the reference object
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Reference Object", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the frame and calculate pixels per cm
            cv2.imshow("Calibration", frame)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                pixels_per_cm = w / ref_width_cm
                print(f"Calibration complete. Pixels per cm: {pixels_per_cm}")
                return pixels_per_cm

        # Show the frame
        cv2.imshow("Calibration", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# Calibrate PIXELS_PER_CM
PIXELS_PER_CM = calibrate_pixels_per_cm()
if PIXELS_PER_CM is None:
    print("Calibration failed. Exiting.")
    exit()

# Constants for size filtering (in centimeters)
MIN_SIZE = 4.0  # Minimum size to detect
MAX_SIZE = 10.0  # Maximum size to detect

# Zoom variables
zoom_level = 1.0
zoom_step = 0.1
max_zoom = 3.0
min_zoom = 1.0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Apply zoom
    h, w, _ = frame.shape
    zoomed_h = int(h / zoom_level)
    zoomed_w = int(w / zoom_level)
    y1 = (h - zoomed_h) // 2
    y2 = y1 + zoomed_h
    x1 = (w - zoomed_w) // 2
    x2 = x1 + zoomed_w

    # Crop and resize for zoom
    cropped_frame = frame[y1:y2, x1:x2]
    frame = cv2.resize(cropped_frame, (w, h), interpolation=cv2.INTER_LINEAR)

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

        # Get rotated bounding box
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = box.astype(int)
        (center_x, center_y), (width, height), angle = rect

        # Convert dimensions to centimeters
        width_cm = width / PIXELS_PER_CM
        height_cm = height / PIXELS_PER_CM

        # Skip objects outside the specified size range
        if width_cm < MIN_SIZE or width_cm > MAX_SIZE or height_cm < MIN_SIZE or height_cm > MAX_SIZE:
            continue

        # Draw rotated bounding box
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        cv2.putText(frame, f"{width_cm:.1f}x{height_cm:.1f} cm", (int(center_x), int(center_y)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Calculate the center of the object using moments
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Convert center to cm
            cx_cm = cx / PIXELS_PER_CM
            cy_cm = cy / PIXELS_PER_CM

            # Draw the center point and display in cm
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, f"Center: ({cx_cm:.1f}, {cy_cm:.1f}) cm", (cx + 10, cy), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Show the frame with the bounding boxes and centers
    cv2.imshow('Real-Time Object Measurement', frame) 

    # Key controls for zoom and quitting
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Quit
        break
    elif key == ord('+') or key == ord('='):  # Zoom in
        zoom_level = min(max_zoom, zoom_level + zoom_step)
    elif key == ord('-') or key == ord('_'):  # Zoom out
        zoom_level = max(min_zoom, zoom_level - zoom_step)

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
