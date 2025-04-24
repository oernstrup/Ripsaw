from flask import Flask, request, render_template
from gpiozero import Servo

app = Flask(__name__)

# Adjust pulse width range depending on your servo
pan = Servo(17, min_pulse_width=0.0005, max_pulse_width=0.0025)
tilt = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    pan_val = float(request.form.get("pan", 0))
    tilt_val = float(request.form.get("tilt", 0))

    pan.value = pan_val
    tilt.value = tilt_val

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
