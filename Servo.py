import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo
servo_pin = 27

# Set PWM parameters
frequency = 50  # Hz (frequency of PWM signal)
duty_cycle_min = 2.5  # Duty cycle for the minimum servo position
duty_cycle_max = 12.5  # Duty cycle for the maximum servo position

# Initialize GPIO pin for servo
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance
pwm = GPIO.PWM(servo_pin, frequency)

# Start PWM
pwm.start(0)

try:
    while True:
        # Move servo to the minimum position
        pwm.ChangeDutyCycle(duty_cycle_min)
        time.sleep(1)  # Wait for the servo to reach the position

        # Move servo to the maximum position
        pwm.ChangeDutyCycle(duty_cycle_max)
        time.sleep(1)  # Wait for the servo to reach the position

except KeyboardInterrupt:
    # Ctrl+C pressed, cleanup GPIO
    pwm.stop()
    GPIO.cleanup()
