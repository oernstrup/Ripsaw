import serial
import time

# Define the correct serial port for Raspberry Pi
SERIAL_PORT = "/dev/serial1"  # Change if needed
BAUD_RATE = 9600
TIMEOUT = 2  # Set a timeout for reading responses

def test_serial():
    """Test communication with Sabertooth motor controller."""

    print(f"[ok] Attempting to open serial port: {SERIAL_PORT} at {BAUD_RATE} baud")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT, write_timeout=1)
        print("[ok] Serial connection established!\n")

    except serial.SerialException as e:
        print(f"[fail] Failed to open serial port: {e}")
        return

    # Sabertooth packet
    ADDRESS = 128  
    COMMAND = 0  
    SPEED = 50  
    CHECKSUM = (ADDRESS + COMMAND + SPEED) & 127  

    # Correct way to construct a raw byte packet
    command_packet = bytes([ADDRESS & 0xFF, COMMAND & 0xFF, SPEED & 0xFF, CHECKSUM & 0xFF])

    print(f"Sending packet (raw): {command_packet}")
    print(f"Sending packet (hex): {command_packet.hex()}")
    print(f"Sending packet  (ASCII): {command_packet.decode(errors='ignore')}")

    try:
        ser.write(command_packet)

        time.sleep(0.1)

        response = ser.read(10)

        if response:
            print(f"Response received (raw): {response}")
            print(f"Response received (hex): {response.hex()}")
            print(f"Response received (ASCII): {response.decode(errors='ignore')}")
        else:
            print("[ℹ️] No response received.")

    except serial.SerialTimeoutException:
        print("[fail] Serial write timeout! Check Sabertooth connection.")
    except Exception as e:
        print(f"[fail] Serial communication error: {e}")

    finally:
        ser.close()
        print("[ok] Serial test complete.")

if __name__ == "__main__":
    test_serial()
