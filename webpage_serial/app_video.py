from flask import Flask, render_template, request, jsonify, Response
import serial
import time
import cv2

app = Flask(__name__)

# Arduino message handler
@app.route("/")
def index():
    return render_template("index_video.html")

@app.route("/send", methods=["POST"])
def send_to_arduino():
    message = request.json.get("message", "")
    try:
        with serial.Serial('/dev/ttyACM0', 9600, timeout=2) as ser:
            time.sleep(2)  # Wait for Arduino reset
            ser.write(message.encode())
            response = ser.readline().decode().strip()
            return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

# Camera stream generator
def gen_frames():
    camera = cv2.VideoCapture(0)  # Use 0 for Pi Camera or USB cam
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Convert frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield in MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
