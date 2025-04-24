from flask import Flask, render_template_string, redirect, url_for
import os
import subprocess
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
            "-t", "1000"  # wait 1 second before capture
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("Error capturing image:", e)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
