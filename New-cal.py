import numpy as np

def Calculation():
    # Coordinate x, y
    PIXELS_PER_CM = float(input('Pixel per cm : '))
    x_o = float(input('x origin : ')) / PIXELS_PER_CM
    y_o = float(input('y origin : ')) / PIXELS_PER_CM
    x = float(input('x of local OJ : ')) / PIXELS_PER_CM
    y = float(input('y of local OJ : ')) / PIXELS_PER_CM
    dz = float(input('z of local OJ : '))
    phi = 0

    # Calculate the differences
    dx = x - x_o
    dy = y - y_o

    def inverse_kinematics(dx, dy, dz, phi):
        l1, l2, l3, l4 = 5, 20, 16, 10  # Link lengths

        if dx == 0 and dy == 0:
            print("Invalid inputs: dx and dy cannot both be zero.")
            return None

        theta0 = np.arctan2(dy, dx)

        A = dx - l4 * np.cos(theta0) * np.cos(phi)
        B = dy - l4 * np.sin(theta0) * np.cos(phi)
        C = dz - l1 - l4 * np.sin(phi)

        cos_theta2 = (A**2 + B**2 + C**2 - l2**2 - l3**2) / (2 * l2 * l3)
        
        # Ensure cos_theta2 is in a valid range
        if not (-1 <= cos_theta2 <= 1):
            print("Target position is out of reach (cos_theta2 out of range).")
            return None

        theta2_1 = np.arccos(cos_theta2)
        theta2_2 = -theta2_1

        solutions = []
        for theta2 in [theta2_1, theta2_2]:
            a = l3 * np.sin(theta2)
            b = l2 + l3 * np.cos(theta2)
            r = np.sqrt(a**2 + b**2)

            discriminant = r**2 - C**2
            if discriminant < 0:
                print("Skipping solution due to negative discriminant (no real solution).")
                continue

            theta1_1 = np.arctan2(C, np.sqrt(discriminant)) - np.arctan2(a, b)
            theta1_2 = np.arctan2(C, -np.sqrt(discriminant)) - np.arctan2(a, b)

            for theta1 in [theta1_1, theta1_2]:
                theta3 = phi - theta1 - theta2
                solutions.append((theta0, theta1, theta2, theta3))

        return solutions

    def to_positive_degrees(angle_rad):
        """ Convert radians to degrees and ensure positive range (0 to 360) """
        angle_deg = np.degrees(angle_rad) % 360  # Convert and ensure within 0-360
        return angle_deg if angle_deg >= 0 else angle_deg + 360  # Handle negatives

    solutions = inverse_kinematics(dx, dy, dz, phi)

    if solutions:
        valid_solutions = []
        for i, (theta0, theta1, theta2, theta3) in enumerate(solutions, start=1):
            # Convert angles to positive degrees
            theta0_deg = to_positive_degrees(theta0)
            theta1_deg = to_positive_degrees(theta1)
            theta2_deg = to_positive_degrees(theta2)
            theta3_deg = to_positive_degrees(theta3)

            # Check if any angle exceeds 270°
            if any(angle > 270 for angle in [theta0_deg, theta1_deg, theta2_deg, theta3_deg]):
                print(f"Solution {i} is invalid (angle > 270°). Skipping...")
                continue  # Skip this solution

            valid_solutions.append((theta0_deg, theta1_deg, theta2_deg, theta3_deg))

        if valid_solutions:
            print("\nValid solutions (theta0, theta1, theta2, theta3):")
            for i, (theta0, theta1, theta2, theta3) in enumerate(valid_solutions, start=1):
                print(f"Solution {i}:")
                print(f"  theta0: {theta0:.2f}°")
                print(f"  theta1: {theta1:.2f}°")
                print(f"  theta2: {theta2:.2f}°")
                print(f"  theta3: {theta3:.2f}°")
        else:
            print("No valid solutions found (all angles exceed 270°).")
    else:
        print("No valid solutions found for the given inputs.")

# Run the calculation function
Calculation()