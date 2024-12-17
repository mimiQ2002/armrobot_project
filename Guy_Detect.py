import cv2
import numpy as np

def detect():
    def nothing(x):
        pass

    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Adjust the HSV trackbars to detect objects. Press ESC to exit.")

    # Create trackbars
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

    prev_coords = None  # To store previous coordinates

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Error: Empty frame captured.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get trackbar positions
        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = max(cv2.getTrackbarPos("U - H", "Trackbars"), l_h)
        u_s = max(cv2.getTrackbarPos("U - S", "Trackbars"), l_s)
        u_v = max(cv2.getTrackbarPos("U - V", "Trackbars"), l_v)

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        # Create a mask
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        output = frame.copy()

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:  # Ignore small contours
                x, y, w, h = cv2.boundingRect(largest_contour)
                cx = x + w // 2
                cy = y + h // 2

                frame_width = frame.shape[1]
                frame_height = frame.shape[0]
                local_cx = cx - frame_width // 2
                local_cy = frame_height // 2 - cy

                # Draw results
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(output, (cx, cy), 5, (0, 255, 255), -1)
                cv2.putText(output, f"Local: ({local_cx}, {local_cy})", (cx - 50, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                # Print coordinates only if they change
                current_coords = (local_cx, local_cy)
                if prev_coords != current_coords:
                    print(f"Local Coordinates: {current_coords}")
                    prev_coords = current_coords

        # Display frames
        cv2.imshow("result", result)
        cv2.imshow("output", output)

        if cv2.waitKey(1) == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

# # Call the function
detect()
