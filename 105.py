## Run on pi only ##
import RPi.GPIO as GPIO ##pip install RPi.GPIO 
from time import sleep

#setup pi 5 for pin for control servo motor
GPIO.setmode(GPIO.BOARD) #setup
GPIO.setup(11, GPIO.OUT) #Connected the servo motor to pin 11 on pi 5 as output mode

#Create PWM 50 Hz signal on that GPIO.PWM(). Start the signal at 0.
pwm = GPIO.PWM(11, 50)
pwm.start(0)

#Use the ChangeDutyCycle() 
pwm.ChangeDutyCycle(5) #left -90 deg position
sleep(1)
pwm.ChangeDutyCycle(7.5) #neutral position (center)
sleep(1)
pwm.ChangeDutyCycle(10) #right +90 deg position

pwm.stop()
GPIO.cleanup

