import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(1)
cv2.namedWindow("Trackbars")

# HSV trackbars
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()
    if not _:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get trackbar values
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    # Avoid upper range values less than lower range values
    u_h = max(u_h, l_h)  # Ensure that upper hue is not less than lower hue
    
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    
    # Create a mask based on the HSV values
    mask = cv2.inRange(hsv, lower, upper)
    
    # Perform bitwise AND to get the result image
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Initialize output to the original frame
    output = frame.copy()

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cx = x + w // 2
        cy = y + h // 2
        
        # Calculate local coordinates
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]
        local_cx = cx - frame_width // 2
        local_cy = frame_height // 2 - cy

        # Draw bounding box, centroid and display coordinates
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(output, (cx, cy), 5, (0, 255, 255), -1)
        cv2.putText(output, f"Local: ({local_cx}, {local_cy})", (cx - 50, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Print local coordinates
        print(f"Local Coordinates: ({local_cx}, {local_cy})")
    
    # Display the frames
    cv2.imshow("frame", frame)
    cv2.imshow("result", result)
    cv2.imshow("output", output)

    # Break loop on ESC key
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
