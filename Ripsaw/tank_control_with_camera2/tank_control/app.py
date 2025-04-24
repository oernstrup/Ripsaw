from flask import Flask, render_template, request, Response
import serial
import threading
import cv2
from picamera2 import Picamera2



picam2 = Picamera2()
picam2.preview_configuration.main.size = (800, 600)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()


app = Flask(__name__)

arduino = serial.Serial('/dev/ttyACM0', 9600)
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


def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)