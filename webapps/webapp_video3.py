from flask import Flask, render_template_string, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Raspberry Pi Camera Stream</title>
</head>
<body>
    <h1>Live Stream</h1>
    <img src="{{ url_for('video_feed') }}" width="800">
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
