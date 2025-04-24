from flask import Flask, render_template_string, redirect, url_for, request
import os
import subprocess
from datetime import datetime
from gpiozero import Servo
from time import sleep

app = Flask(__name__)
PHOTO_PATH = "static/capture.jpg"

# GPIO pins for servo
# Adjust `min_pulse_width` and `max_pulse_width` if needed
pan_servo = Servo(17, min_pulse_width=0.0006, max_pulse_width=0.0023)
tilt_servo = Servo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)

# Current position from -1 (left/up) to 1 (right/down)
servo_pos = {"pan": 0, "tilt": 0}

def move_servo(axis, step):
    servo_pos[axis] += step
    servo_pos[axis] = max(-1, min(1, servo_pos[axis]))  # Clamp to range

    if axis == "pan":
        pan_servo.value = servo_pos["pan"]
    elif axis == "tilt":
        tilt_servo.value = servo_pos["tilt"]
    sleep(0.2)

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Raspberry Pi Camera</title>
    <script>
        document.addEventListener('keydown', function(event) {
            let direction = null;
            if (event.key === 'ArrowLeft') direction = 'left';
            else if (event.key === 'ArrowRight') direction = 'right';
            else if (event.key === 'ArrowUp') direction = 'up';
            else if (event.key === 'ArrowDown') direction = 'down';

            if (direction) {
                fetch('/move', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: 'direction=' + direction
                }).then(() => location.reload());
                event.preventDefault();
            }
        });
    </script>
</head>
<body>
    <h1>Raspberry Pi Camera Webpage</h1>
    <form action="/capture" method="post">
        <button type="submit">📷 Take Picture</button>
    </form>

    <h2>Camera Pan/Tilt Control</h2>
    <form action="/move" method="post">
        <button name="direction" value="left">⬅️ Left</button>
        <button name="direction" value="right">➡️ Right</button>
        <button name="direction" value="up">⬆️ Up</button>
        <button name="direction" value="down">⬇️ Down</button>
    </form>

    <p>Use arrow keys on your keyboard to move the camera!</p>

    {% if photo %}
        <h2>Latest Picture:</h2>
        <img src="{{ url_for('static', filename='capture.jpg') }}?t={{ timestamp }}" width="1024">
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    photo_exists = os.path.exists(PHOTO_PATH)
    return render_template_string(HTML_PAGE, photo=photo_exists, timestamp=datetime.now().timestamp())

@app.route("/capture", methods=["POST"])
def capture():
    os.makedirs("static", exist_ok=True)
    try:
        subprocess.run([
            "raspistill",
            "-o", PHOTO_PATH,
            "-w", "1024",
            "-h", "768",
            "-t", "1000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("Error capturing image:", e)
    return redirect(url_for('index'))

@app.route("/move", methods=["POST"])
def move_servo_route():
    direction = request.form.get("direction")
    step = 0.1  # Step size for smooth control

    if direction == "left":
        move_servo("pan", -step)
    elif direction == "right":
        move_servo("pan", step)
    elif direction == "up":
        move_servo("tilt", -step)
    elif direction == "down":
        move_servo("tilt", step)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
