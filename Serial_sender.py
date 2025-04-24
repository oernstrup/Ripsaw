import serial
print("Start")
ser = serial.Serial('/dev/ttyACM0', 9600)  # Open serial connection
ser.write(b'Hello Arduino')  # Send data
print(ser.readline())  # Read response
ser.close()
print("End")