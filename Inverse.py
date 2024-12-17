import math

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
    l1, l2, l3, l4 = 4.5, 20.0, 20.0, 4.5

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
    return tuple(map(radians_to_degrees, [theta1, theta2, theta3, theta4]))

def main():
    try:
        # Get input from the user
        dx = float(input("Enter dx (x-coordinate of the end effector): "))
        dy = float(input("Enter dy (y-coordinate of the end effector): "))
        dz = float(input("Enter dz (z-coordinate of the end effector): "))
        # phi = float(input("Enter phi (orientation angle in radians): "))
        phi = math.pi*3/4

        joint_angles = inverse_kinematics(dx, dy, dz, phi)
        print("Joint Angles (in degrees):", joint_angles)
    except ValueError as e:
        print("Invalid input or error in calculation:", e)

if __name__ == "__main__":
    main()
