from adafruit_servokit import ServoKit 
import board
import time  # Import time module for sleep functionality

def ControlServo():
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

    def get_joint_angle(joint_id):
        """ Get validated input for a joint angle """
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

    def configure_servos(kit):
        """ Configure servos with actuation range and pulse width """
        for i in range(5):
            kit.servo[i].actuation_range = 270  # Example: Max 270 degrees
            kit.servo[i].set_pulse_width_range(500, 2500)  # Set pulse width range

    def move_joints(kit, joints):
        """ Move joints to specified angles one degree at a time """
        for i, target_angle in enumerate(joints):
            current_angle = kit.servo[i].angle if kit.servo[i].angle is not None else 0
            step = 1 if target_angle > current_angle else -1
            print(f"Moving joint {i} from {current_angle} to {target_angle} degrees.")
            for angle in range(current_angle, target_angle, step):
                kit.servo[i].angle = angle
                time.sleep(0.01)  # Small delay for smooth movement
            kit.servo[i].angle = target_angle  # Ensure final position is set
            print(f"Setting joint {i} to {target_angle} degrees.")
            time.sleep(2)  # Delay to allow movement

    def return_to_original_positions(kit, jog):
        """ Return joints to original (calibrated) positions """
        print("\nReturning to original positions...")
        time.sleep(3)  # Short wait before returning

        for i, target_angle in enumerate(jog):
            current_angle = kit.servo[i].angle if kit.servo[i].angle is not None else 0
            step = 1 if target_angle > current_angle else -1
            print(f"Returning joint {i} from {current_angle} to {target_angle} degrees.")
            for angle in range(current_angle, target_angle, step):
                kit.servo[i].angle = angle
                time.sleep(0.01)  # Small delay for smooth movement
            kit.servo[i].angle = target_angle  # Ensure final position is set
            print(f"Setting joint {i} back to {target_angle} degrees.")
            time.sleep(2)  # Delay for each joint movement

    # Get input for all joints
    joints = [get_joint_angle(i) for i in range(5)]
    print(joints)

    # Initialize the ServoKit with 16 channels
    kit = ServoKit(channels=16)

    # Configure servos (set once)
    configure_servos(kit)

    # Move joints to input positions
    move_joints(kit, joints)

    # Return to original (calibrated) positions
    return_to_original_positions(kit, jog)

    print("\nAll done!!")

# Call the function
ControlServo()