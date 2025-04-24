from flask import Flask, render_template_string, Response, redirect, url_for
from picamera import PiCamera
from time import sleep
from io import BytesIO
import threading
import os
from datetime import datetime

app = Flask(__name__)
camera = PiCamera()
camera.resolution = (1280, 720)
PHOTO_PATH = "static/capture.jpg"

# HTML Template
HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Pi Camera Stream</title>
</head>
<body>
    <h1>Live Video from Raspberry Pi</h1>
    <img src="{{ url_for('video_feed') }}" width="1280" height="720">
    <form action="/capture" method="post">
        <button type="submit">📷 Take Picture</button>
    </form>
    {% if photo %}
        <h2>Last Captured Image:</h2>
        <img src="{{ url_for('static', filename='capture.jpg') }}?t={{ timestamp }}" width="1280">
    {% endif %}
</body>
</html>
"""

def generate_stream():
    stream = BytesIO()
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        frame = stream.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        stream.seek(0)
        stream.truncate()

@app.route("/")
def index():
    return render_template_string(HTML_PAGE,
                                  photo=os.path.exists(PHOTO_PATH),
                                  timestamp=datetime.now().timestamp())

@app.route("/video_feed")
def video_feed():
    return Response(generate_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/capture", methods=["POST"])
def capture():
    camera.capture(PHOTO_PATH)
    return redirect(url_for('index'))

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    camera.start_preview()
    sleep(2)  # Give camera time to warm up
    app.run(host='0.0.0.0', port=5000, debug=True)
