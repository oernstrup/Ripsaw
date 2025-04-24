import serial
import time

# Initialize bidirectional serial connection to Sabertooth 2x12
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1, write_timeout=1)  # Bi-directional communication

def motor_control(motor, speed):
    """
    Controls a motor via Sabertooth 2x12 using bidirectional serial communication.

    :param motor: Motor number (1 or 2)
    :param speed: Speed (-127 to 127), where:
                  - 127 = Full forward
                  - 0   = Stop
                  - -127 = Full reverse
    """
    if motor == 1:
        print("Motor 1")
        command = 0 if speed >= 0 else 1  # Motor 1 Forward (0) or Reverse (1)
    elif motor == 2:
        print("Motor 2")
        command = 4 if speed >= 0 else 5  # Motor 2 Forward (4) or Reverse (5)
    else:
        print("Invalid motor number! Use 1 or 2.")
        return

    # Ensure speed is within the valid range (0 to 127)
    speed = min(127, max(0, abs(speed)))  # Absolute speed, 0 to 127

    # Construct the command packet
    serial_command = bytes([command, speed])

    try:
        ser.write(serial_command)
        #time.sleep(0.1)  # Small delay for execution
        time.sleep(1)  # Small delay for execution
        # Read response (if Sabertooth supports bidirectional feedback)
        response = ser.read(10)  # Read up to 10 bytes of response data
        if response:
            print(f"Sabertooth Response hex: {response.hex()}")
           # print(f"Sabertooth Response text: ",response)
    
    except serial.SerialTimeoutException:
        print("Serial write timeout! Ensure Sabertooth is connected.")
    except Exception as e:
        print(f"Serial communication error: {e}")

def stop_motors():
    """Stops both motors by sending the correct stop signal."""
    motor_control(1, 0)  # Stop motor 1
    motor_control(2, 0)  # Stop motor 2
    print("Motors stopped.")

try:
    print("Starting motor control...")
    while True:
        user_input = input("Enter command (1=Forward, 2=Backward, 3=Stop, q=Quit): ").strip().lower()

        if user_input == "1":
            motor_control(1, 50)  # Forward with speed 50
            motor_control(2, 50)
            print("Motors moving forward.")

        elif user_input == "2":
            motor_control(1, -50)  # Backward with speed -50
            motor_control(2, -50)
            print("Motors moving backward.")

        elif user_input == "3":
            stop_motors()  # Call the stop function

        elif user_input == "q":
            stop_motors()
            print("Stopping motors and exiting...")
            break

        else:
            print("Invalid input! Use 1, 2, 3, or q.")

except KeyboardInterrupt:
    print("\nStopping motors due to Keyboard Interrupt...")
    stop_motors()

finally:
    ser.close()
