from flask import Flask, render_template_string, Response, request
from picamera2 import Picamera2
from gpiozero import Servo
from time import sleep
import cv2

app = Flask(__name__)

# Setup servos (you may need to calibrate min/max pulses)
pan = Servo(17)
tilt = Servo(27)

# Initial positions (centered)
pan_pos = 0.0
tilt_pos = 0.0
pan.value = pan_pos
tilt.value = tilt_pos

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Raspberry Pi Camera Stream with Pan-Tilt</title>
</head>
<body>
    <h1>Live Camera Feed with Pan-Tilt Control</h1>
    <img src="{{ url_for('video_feed') }}" width="800"><br><br>
    
    <form action="/move" method="post">
        <button name="dir" value="up">⬆️</button><br>
        <button name="dir" value="left">⬅️</button>
        <button name="dir" value="center">⏺️</button>
        <button name="dir" value="right">➡️</button><br>
        <button name="dir" value="down">⬇️</button>
    </form>
</body>
</html>
"""

picam2 = Picamera2()
picam2.preview_configuration.main.size = (800, 600)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move', methods=['POST'])
def move():
    global pan_pos, tilt_pos
    direction = request.form.get("dir")

    step = 0.1  # adjust as needed

    if direction == "up":
        tilt_pos = max(-1.0, tilt_pos - step)
    elif direction == "down":
        tilt_pos = min(1.0, tilt_pos + step)
    elif direction == "left":
        pan_pos = max(-1.0, pan_pos - step)
    elif direction == "right":
        pan_pos = min(1.0, pan_pos + step)
    elif direction == "center":
        pan_pos = 0.0
        tilt_pos = 0.0

    pan.value = pan_pos
    tilt.value = tilt_pos
    sleep(0.05)

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
