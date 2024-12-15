from adafruit_servokit import ServoKit

# Initialize the ServoKit instance for a 16-channel servo driver
kit = ServoKit(channels=16)

# Configure servos (0-4) to support 0°–270° motion
for i in range(5):  # Channels 0 to 4
    kit.servo[i].actuation_range = 270  # Set the actuation range to 270°
    kit.servo[i].set_pulse_width_range(500, 2500)  # Set custom pulse width range

# Move servos to specific angles
servo_angles = [0, 90, 135, 180, 270]  # Angles for servos 0 to 4
try:
    for i in range(5):
        print(f"Setting Servo {i} to {servo_angles[i]}°")
        kit.servo[i].angle = servo_angles[i]  # Set servo angle
except KeyboardInterrupt:
    print("Program interrupted.")

