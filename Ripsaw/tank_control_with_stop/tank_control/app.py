from flask import Flask, render_template, request
import serial
import threading

app = Flask(__name__)

arduino = serial.Serial('/dev/ttyACM0', 9600)  # Updated to ACM0 for many Arduinos
lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    direction = request.form.get('direction')
    speed = request.form.get('speed', type=int)

    if direction and speed is not None:
        command = f"{direction}{speed}\n"
        with lock:
            arduino.write(command.encode())
        return 'OK', 200
    return 'Invalid', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)