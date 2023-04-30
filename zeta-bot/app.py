from flask import Flask, render_template, request, redirect, url_for, Response
import os
import yaml
import cv2
import time
from datetime import datetime

app = Flask(__name__)

camera_list = []

camera_ids = ['/dev/video0', '/dev/video2']

for camera_id in camera_ids:
    camera = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    camera.set(cv2.CAP_PROP_FPS, 30)
    camera_list.append(camera)

def gen(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.033)  # 0.033 seconds for a 30 FPS video stream


def write_config_to_file(prefix, config):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename_number = 1

    while True:
        filename_template = f"{prefix}_{timestamp}_{filename_number:03d}.yaml"
        file_path = os.path.join("messages", filename_template)

        if not os.path.exists(file_path):
            break
        filename_number += 1

    with open(file_path, "w") as outfile:
        yaml.dump(config, outfile)

@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    return Response(gen(camera_list[camera_index]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_movement', methods=['POST'])
def set_movement():
    rpm = int(request.form['rpm'])
    distance = float(request.form['distance'])

    data = {
        "rpm": rpm,
        "distance": distance
    }

    write_config_to_file("bot_move", data)
    return redirect(url_for('index'))

@app.route('/set_rotation', methods=['POST'])
def set_rotation():
    rpm = int(request.form['rpm'])
    direction_fl = request.form['direction_fl']
    direction_bl = request.form['direction_bl']
    direction_fr = request.form['direction_fr']
    direction_br = request.form['direction_br']
    target_rotation = float(request.form['target_rotation'])

    data = {
        "rpm": rpm,
        "direction_fl": direction_fl,
        "direction_bl": direction_bl,
        "direction_fr": direction_fr,
        "direction_br": direction_br,
        "target_rotation": target_rotation
    }

    write_config_to_file("bot_rotate", data)
    return redirect(url_for('index'))

@app.route('/set_servo_position', methods=['POST'])
def set_servo_position():
    servo_name = request.form['servo_name']
    angle = int(request.form['angle'])

    data = {
        "servo_name": servo_name,
        "angle": angle
    }

    write_config_to_file("bot_servo", data)
    return redirect(url_for('index'))

@app.route('/get_measurement', methods=['POST'])
def get_measurement():
    sensor_name = request.form['sensor_name']

    data = {
        "sensor_name": sensor_name
    }

    write_config_to_file("bot_ultrasonic", data)
    return redirect(url_for('index'))

@app.route('/quit', methods=['POST'])
def quit():
    return redirect(url_for('index'))
