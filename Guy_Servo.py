from adafruit_servokit import ServoKit
import board
import time  # Import time module for sleep functionality

# Define valid ranges for each joint
valid_ranges = {
    0: (0, 180),     # Example range for joint 0
    1: (0, 180),     # Example range for joint 1
    2: (0, 250),     # Joint 2 has a maximum of 250
    3: (0, 140),     # Joint 3 has a maximum of 140
    4: (0, 180)      # Gripper, example range
}

# Function to get validated input
def get_joint_angle(joint_id):
    min_angle, max_angle = valid_ranges[joint_id]
    while True:
        try:
            angle = int(input(f"Input degree for joint {joint_id} (range {min_angle}-{max_angle}): "))
            if min_angle <= angle <= max_angle:
                return angle
            else:
                print(f"!!! Input degree out of range ({min_angle}-{max_angle}) !!!")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Get input for all joints
joints = [get_joint_angle(i) for i in range(5)]

# Initialize the ServoKit with 16 channels
kit = ServoKit(channels=16)

# Configure servos if needed
for i in range(5):
    kit.servo[i].actuation_range = 270  # Example: Set actuation range to 180 degrees
    kit.servo[i].set_pulse_width_range(500, 2500)  # Example: Adjust pulse width range

# Set each servo to its corresponding joint angle
for i, angle in enumerate(joints):
    kit.servo[i].angle = angle
    print(f"Setting joint {i} to {angle} degrees.")
    time.sleep(2)  # Add a 2-second delay for each joint
