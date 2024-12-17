import cv2
import numpy as np

# Initialize the webcam


def calibrate_pixels_per_cm():
    cap = cv2.VideoCapture(0)  # Use 0 for default camera
    print("Please place a reference object of known width in front of the camera.")
    ref_width_cm = float(input("Enter the width of the reference object in cm: "))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) < 100:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Reference Object", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow("Calibration", frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                pixels_per_cm = w / ref_width_cm
                print(f"Calibration complete. Pixels per cm: {pixels_per_cm}")
                cap.release()
                cv2.destroyAllWindows()
                return pixels_per_cm

        cv2.imshow("Calibration", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    # return None

    if __name__ == "__main__":
        # Calibration
        PIXELS_PER_CM = calibrate_pixels_per_cm()
        if PIXELS_PER_CM is None or PIXELS_PER_CM <= 0:
            print("Calibration failed. Exiting.")
            exit()

        # Constants
        MIN_SIZE = 4.0
        MAX_SIZE = 10.0
        zoom_level = 1.0
        zoom_step = 0.1
        max_zoom = 3.0
        min_zoom = 1.0

        # Reinitialize the webcam
        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply zoom
            h, w, _ = frame.shape
            zoomed_h = min(h, int(h / zoom_level))
            zoomed_w = min(w, int(w / zoom_level))
            y1 = (h - zoomed_h) // 2
            y2 = y1 + zoomed_h
            x1 = (w - zoomed_w) // 2
            x2 = x1 + zoomed_w

            cropped_frame = frame[y1:y2, x1:x2]
            frame = cv2.resize(cropped_frame, (w, h), interpolation=cv2.INTER_LINEAR)

            # Grayscale and threshold
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect).astype(int)
                (center_x, center_y), (width, height), angle = rect

                width_cm = width / PIXELS_PER_CM
                height_cm = height / PIXELS_PER_CM

                if width_cm < MIN_SIZE or width_cm > MAX_SIZE or height_cm < MIN_SIZE or height_cm > MAX_SIZE:
                    continue

                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                cv2.putText(frame, f"{width_cm:.1f}x{height_cm:.1f} cm", 
                            (int(center_x), int(center_y)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

            cv2.imshow('Real-Time Object Measurement', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('+'):
                zoom_level = min(max_zoom, zoom_level + zoom_step)
            elif key == ord('-'):
                zoom_level = max(min_zoom, zoom_level - zoom_step)

        cap.release()
        cv2.destroyAllWindows()

