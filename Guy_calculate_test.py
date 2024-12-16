import numpy as np
import math

# Coordinate x, y
x_o = float(input('x origin : '))  # Convert input to float
y_o = float(input('y origin : '))  # Convert input to float
x = float(input('x of local OJ : '))  # Convert input to float
y = float(input('y of local OJ : '))  # Convert input to float
phi = np.pi/2

# Calculate the differences
dx = x - x_o
dy = y - y_o

def radians_to_degrees(radians):
    """
    Convert radians to degrees.
    """
    return radians * (180.0 / math.pi)

def inverse_kinematics(dx, dy, dz, phi):
    """
    Solve the inverse kinematics for a 4-DOF robotic arm.

    Parameters:
    dx, dy, dz : float
        Coordinates of the end effector in the global frame.
    phi : float
        Orientation angle of the end effector.

    Returns:
    tuple
        Joint angles (theta1, theta2, theta3, theta4) in degrees.
    """
    # Lengths of the links (adjust according to your robot's dimensions)
    l1, l2, l3, l4 = 5, 20.0, 16, 10

    # Calculate theta1
    theta1 = math.atan2(dy, dx)

    # Intermediate variables for theta2 and theta3
    r = math.sqrt(dx**2 + dy**2)
    a = dz - l1
    b = math.sqrt(r**2 + a**2)
    c = l2
    d = l3

    # Ensure cos_theta2 is within the valid range for acos
    cos_theta2 = (b**2 + c**2 - d**2) / (2 * b * c)
    cos_theta2 = max(min(cos_theta2, 1.0), -1.0)

    theta2_options = [math.acos(cos_theta2), -math.acos(cos_theta2)]

    theta2_results = []
    for theta2 in theta2_options:
        # Calculate theta3 for each theta2
        cos_theta3 = (c**2 + d**2 - b**2) / (2 * c * d)
        cos_theta3 = max(min(cos_theta3, 1.0), -1.0)
        theta3 = math.acos(cos_theta3)

        # Add to results
        theta2_results.append((theta2, theta3))

    # For simplicity, we'll select the first valid solution
    theta2, theta3 = theta2_results[0]

    # Calculate theta4 based on phi
    theta4 = phi - theta2 - theta3

    # Convert all angles to degrees
    theta1_deg = radians_to_degrees(theta1)
    theta2_deg = radians_to_degrees(theta2)
    theta3_deg = radians_to_degrees(theta3)
    theta4_deg = radians_to_degrees(theta4)

    # Print each theta value
    print(f"Theta1: {theta1_deg:.2f} degrees")
    print(f"Theta2: {theta2_deg:.2f} degrees")
    print(f"Theta3: {theta3_deg:.2f} degrees")
    print(f"Theta4: {theta4_deg:.2f} degrees")

    return (theta1_deg, theta2_deg, theta3_deg, theta4_deg)

if __name__ == "__main__":
    # Provide dz and phi for inverse kinematics calculation
    dz = float(input('Enter dz (z coordinate of end effector): '))
    # phi = float(input('Enter phi (orientation angle of end effector in radians): '))

    # Call the inverse kinematics function
    angles = inverse_kinematics(dx, dy, dz, phi)
    print(f"Calculated joint angles (theta1, theta2, theta3, theta4): {angles}")
