from flask import Flask, Response, render_template_string
import subprocess

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Raspberry Pi Camera</title>
</head>
<body>
    <h1>Raspberry Pi Live Camera Stream</h1>
    <img src="{{ url_for('video_feed') }}" width="800">
</body>
</html>
"""

def generate_frames():
    # Launch libcamera-vid to produce MJPEG stream via subprocess
    command = [
        "libcamera-vid",
        "--stdout",
        "-t", "0",  # run indefinitely
        "--codec", "mjpeg",
        "--width", "800",
        "--height", "600",
        "--inline"
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)

    try:
        while True:
            chunk = process.stdout.read(1024)
            if not chunk:
                break
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + chunk + b"\r\n")
    except GeneratorExit:
        process.terminate()
    finally:
        process.terminate()

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
