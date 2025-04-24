import serial
import time

# Initialize serial connection to Sabertooth 2x12
ser = serial.Serial('/dev/serial0', 9600, timeout=1)  # Use '/dev/serial0' for Raspberry Pi UART

def motor_control(motor, speed):
    """
    Controls a motor via Sabertooth 2x12 in Simplified Serial Mode.
    
    :param motor: Motor number (1 or 2)
    :param speed: Speed (-127 to 127), where:
                  - 127 = Full forward
                  - 0   = Stop
                  - -127 = Full reverse
    """
    if motor == 1:
        command = 0 if speed >= 0 else 1
        speed = abs(speed)
    elif motor == 2:
        command = 4 if speed >= 0 else 5
        speed = abs(speed)
    else:
        print("Invalid motor number! Use 1 or 2.")
        return

    speed = min(127, max(0, speed))  # Ensure speed is within valid range
    serial_command = bytes([command, speed])
    ser.write(serial_command)
    time.sleep(0.1)  # Small delay for command execution

try:
    print("Starting motor control...")
    while True:
        user_input = input("Enter command (1=Forward, 2=Backward, 3=Stop, q=Quit): ").strip().lower()

        if user_input == "1":
            motor_control(1, 30)  # Forward with speed 80
            motor_control(2, 30)
        elif user_input == "2":
            motor_control(1, -30)  # Backward with speed -80
            motor_control(2, -30)
        elif user_input == "3":
            motor_control(1, 0)  # Stop
            motor_control(2, 0)
        elif user_input == "q":
            motor_control(1, 0)
            motor_control(2, 0)
            print("Stopping motors and exiting...")
            break
        else:
            print("Invalid input! Use 1, 2, 3, or q.")

except KeyboardInterrupt:
    print("\nStopping motors...")
    motor_control(1, 0)
    motor_control(2, 0)

finally:
    ser.close()