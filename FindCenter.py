import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

# Set frame width and height
cap.set(3, 640)
cap.set(4, 640)

while True:
    _, frame = cap.read()  # Read frame from camera
    
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the color range for blue
    lower_blue = np.array([90, 60, 0])
    upper_blue = np.array([121, 255, 255])
    
    # Create a binary mask for the blue color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Find contours in the mask
    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
        area = cv2.contourArea(c)  # Calculate the area of the contour
        
        if area > 0:  # Process only non-zero area contours
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)  # Draw the contour
            
            M = cv2.moments(c)  # Calculate moments
            
            if M["m00"] != 0:
                # Calculate the centroid of the contour
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Draw a circle at the centroid
                cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
                # Label the centroid
                cv2.putText(frame, "Center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                
                # Print area and centroid
                print("Area is:", area)
                print("Centroid is at:", cx, cy)
    
    # Show the processed frame
    cv2.imshow("frame", frame)
    
    # Break the loop when 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
