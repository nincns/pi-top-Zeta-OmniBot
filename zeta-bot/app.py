#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, Response
import os
import yaml
from datetime import datetime
from camera import MultiCamera

app = Flask(__name__)

multicamera = MultiCamera(video_sources=[0, 2])

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

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera, src):
    while True:
        frame = camera.get_frame(src)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed1')
def video_feed1():
    multicamera.start()
    return Response(gen(multicamera, 0),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    multicamera.start()
    return Response(gen(multicamera, 2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

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
    target_rotation = float(request.form['target_rotation'])

    data = {
        "rpm": rpm,
        "target_rotation": target_rotation
    }

    directions = {}

    for direction in ['fl', 'bl', 'fr', 'br']:
        value = request.form.get(f'direction_{direction}')
        if value:
            directions[f'direction_{direction}'] = value

    data.update(directions)
    
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
