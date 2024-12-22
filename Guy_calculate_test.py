import numpy as np
import math

def Calculattion():
    """Main function to calculate joint angles."""
    # Coordinate x, y
    PIXELS_PER_CM = float(input('Pixel per cm: '))
    x_o = float(input('x origin: ')) / PIXELS_PER_CM
    y_o = float(input('y origin: ')) / PIXELS_PER_CM
    x_oj = float(input('x of local OJ: ')) / PIXELS_PER_CM
    y_oj = float(input('y of local OJ: ')) / PIXELS_PER_CM
    z = 9.5

    # Calculate the differences
    dx = x_oj - x_o
    dy = y_oj - y_o

    # Perform inverse kinematics
    angles = inverse_kinematics(dx, dy, z)
    if angles:
        print(f"Calculated joint angles (theta0, theta1, theta2, theta3): {angles}")
    def radians_to_degrees(radians):
        """Convert radians to degrees."""
        return radians * (180.0 / math.pi)


    def inverse_kinematics(dx, dy, dz):
        """Perform inverse kinematics calculation."""
        l1, l2, l3, l4 = 5, 20, 16, 10  # Link lengths

        # Validate dx and dy
        if dx == 0 and dy == 0:
            print("Invalid inputs: dx and dy cannot both be zero.")
            return None

        # Calculate S
        S = math.sqrt(dx**2 + dy**2)
        # Calculate zeta
        zeta = math.atan2(dy, dx)

        # Calculate ddx and ddy
        ddx = math.sqrt(dx**2 + dz**2)
        ddy = dz - l1

        # Calculate alpha
        alpha = math.atan2(ddy, ddx)

        # Calculate theta0
        theta0 = math.atan2(dy, dx)

        # Adjust dx and dy for theta2 calculation
        dx_adjusted = ddx - l4 * math.cos(alpha)
        dy_adjusted = ddy - l4 * math.sin(alpha)

        # Calculate theta2
        cos_theta2 = (l2**2 + l3**2 - dx_adjusted**2 - dy_adjusted**2) / (2 * l2 * l3)
        if abs(cos_theta2) > 1:
            print("Invalid configuration: cos_theta2 out of range.")
            return None
        theta2 = math.pi - math.acos(cos_theta2)

        # Calculate theta1
        cos_theta1 = (dx_adjusted**2 + dy_adjusted**2 + l2**2 - l3**2) / (2 * S * l2)
        if abs(cos_theta1) > 1:
            print("Invalid configuration: cos_theta1 out of range.")
            return None
        theta1 = math.acos(cos_theta1) + zeta

        # Calculate theta3
        theta3 = alpha - theta1 - theta2

        # Convert to degrees
        theta0_deg = int(radians_to_degrees(theta0))
        theta1_deg = int(radians_to_degrees(theta1))
        theta2_deg = int(radians_to_degrees(theta2))
        theta3_deg = int(radians_to_degrees(theta3))

        print(f"theta0: {theta0_deg:.2f} degrees")
        print(f"theta1: {theta1_deg:.2f} degrees")
        print(f"theta2: {theta2_deg:.2f} degrees")
        print(f"theta3: {theta3_deg:.2f} degrees")

        return theta0_deg, theta1_deg, theta2_deg, theta3_deg






Calculattion()


Calculattion()
