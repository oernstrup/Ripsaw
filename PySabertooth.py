import time
from pysabertooth import Sabertooth

print("[START] Initializing Sabertooth connection...")

try:
    # Define Sabertooth serial connection
    SERIAL_PORT = '/dev/ttyAMA0'  # Change to '/dev/ttyAMA0' if needed
    sabertooth = Sabertooth(SERIAL_PORT, baudrate=9600, address=128, timeout=0.1)

    print("[OK] Sabertooth connection established.")

    # Move motors forward
    print("[INFO] Moving motors forward at speed 50.")
    sabertooth.drive(1, 50)  # Motor 1 forward at speed 50
    sabertooth.drive(2, 50)  # Motor 2 forward at speed 50

    time.sleep(2)  # Run motors for 2 seconds

    # Ensure motors stop before closing connection
    print("[INFO] Stopping motors.")
    sabertooth.stop()

except Exception as e:
    print(f"[ERROR] Communication error: {e}")

finally:
    print("[INFO] Closing Sabertooth serial connection.")
    sabertooth.close()
    print("[OK] Serial communication closed.")

# Ensure the object is properly deleted
del sabertooth
