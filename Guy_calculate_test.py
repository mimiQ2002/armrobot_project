import numpy as np
import math

def Calculattion():
    # Coordinate x, y
    PIXELS_PER_CM = float(input('Pixel per cm : '))
    x_o = float(input('x origin : ')) / PIXELS_PER_CM
    y_o = float(input('y origin : ')) / PIXELS_PER_CM
    x = float(input('x of local OJ : ')) / PIXELS_PER_CM
    y = float(input('y of local OJ : ')) / PIXELS_PER_CM
    phi = np.pi / 2

    # Calculate the differences
    dx = x - x_o
    dy = y - y_o

    def radians_to_degrees(radians):
        return radians * (180.0 / math.pi)

    def inverse_kinematics(dx, dy, dz, phi):
        l1, l2, l3, l4 = 5, 20.0, 16, 10  # Link lengths

        # Validate dx and dy
        if dx == 0 and dy == 0:
            print("Invalid inputs: dx and dy cannot both be zero.")
            return None

        # Calculate theta0
        theta0 = math.atan2(dy, dx)

        # Intermediate variables
        r = math.sqrt(dx**2 + dy**2)
        a = dz - l1
        b = math.sqrt(r**2 + a**2)
        c, d = l2, l3

        # Check for reachability
        if b > l2 + l3 or b < abs(l2 - l3):
            print("Target position is unreachable with the given link lengths.")
            return None

        # Calculate theta1
        cos_theta1 = (b**2 + c**2 - d**2) / (2 * b * c)
        cos_theta1 = max(min(cos_theta1, 1.0), -1.0)
        theta1 = math.acos(cos_theta1)

        # Calculate theta2
        cos_theta2 = (c**2 + d**2 - b**2) / (2 * c * d)
        cos_theta2 = max(min(cos_theta2, 1.0), -1.0)
        theta2 = math.acos(cos_theta2)

        # Calculate theta3
        theta3 = phi - theta1 - theta2

        # Convert to degrees
        theta0_deg = int(115 - radians_to_degrees(theta0))
        theta1_deg = int(100 - radians_to_degrees(theta1))
        theta2_deg = int(100 - radians_to_degrees(theta2))
        theta3_deg = int(90 + radians_to_degrees(theta3))

        print(f"theta0: {theta0_deg:.2f} degrees")
        print(f"theta1: {theta1_deg:.2f} degrees")
        print(f"theta2: {theta2_deg:.2f} degrees")
        print(f"theta3: {theta3_deg:.2f} degrees")

        return (theta0_deg, theta1_deg, theta2_deg, theta3_deg)

    if __name__ == "__main__":
        dz = float(input('Enter dz (z coordinate of end effector): '))
        angles = inverse_kinematics(dx, dy, dz, phi)
        if angles:
            print(f"Calculated joint angles (theta0, theta1, theta2, theta3): {angles}")

Calculattion()