from adafruit_servokit import ServoKit 
import board
import time  # Import time module for sleep functionality

# Degree of joints from calibration
j0_0 = 90  # Base (fixed)
j0_1 = 0 
j0_2 = 30
j0_3 = 30
j0_4 = 0  # Gripper (fixed)

jog = [j0_0, j0_1, j0_2, j0_3, j0_4]

# Define valid ranges for each joint
valid_ranges = {
    0: (0, 360),   # Joint 0: Example range
    1: (0, 45),   # Joint 1
    2: (0, 90),   # Joint 2: Max of 250
    3: (0, 90),   # Joint 3: Max of 140
    4: (0, 30)    # Gripper
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

# Configure servos (set once)
for i in range(5):
    kit.servo[i].actuation_range = 270  # Example: Max 270 degrees
    kit.servo[i].set_pulse_width_range(500, 2500)  # Set pulse width range

# Move joints to input positions
for i, angle in enumerate(joints):
    kit.servo[i].angle = angle
    print(f"Setting joint {i} to {angle} degrees.")
    time.sleep(2)  # Delay to allow movement

# Return to original (calibrated) positions
print("\nReturning to original positions...")
time.sleep(3)  # Short wait before returning

for i, angle in enumerate(jog):
    kit.servo[i].angle = angle
    print(f"Setting joint {i} back to {angle} degrees.")
    time.sleep(2)  # Delay for each joint movement

print("\nAll done!!")
