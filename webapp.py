from flask import Flask, render_template_string, redirect, url_for
import cv2
import os
from datetime import datetime

app = Flask(__name__)
PHOTO_PATH = "static/capture.jpg"

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Raspberry Pi Camera</title>
</head>
<body>
    <h1>Raspberry Pi Camera Webpage</h1>
    <p>Click the button below to take a picture.</p>
    <form action="/capture" method="post">
        <button type="submit">📷 Take Picture</button>
    </form>
    {% if photo %}
        <h2>Latest Picture:</h2>
        <img src="{{ url_for('static', filename='capture.jpg') }}?t={{ timestamp }}" width="400">
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
    cap = cv2.VideoCapture(0)  # 0 for Pi Camera or USB cam
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return redirect(url_for('index'))

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(PHOTO_PATH, frame)
    cap.release()
    return redirect(url_for('index'))

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
