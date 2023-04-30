#!/usr/bin/env python3
import os
import time
import yaml
from pitop import ServoMotor
from glob import glob
import shutil
from datetime import datetime

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def process_servo_command(filepath):
    servo_command = read_yaml_file(filepath)
    servo_name = servo_command['servo_name']
    angle = int(servo_command['angle'])

    servo = ServoMotor(servo_name)
    servo.target_angle = angle
    servo.smooth_acceleration = True

    write_servo_info_to_file(servo_name, angle)

def write_servo_info_to_file(servo_name, angle):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename_number = 1

    while True:
        filename_template = f"msg_bot_servo_{timestamp}_{filename_number:03d}.yaml"
        file_path = os.path.join('messages', filename_template)

        if not os.path.exists(file_path):
            break
        filename_number += 1

    servo_info = {
        "servo_name": servo_name,
        "angle": angle
    }

    with open(file_path, "w") as outfile:
        yaml.dump(servo_info, outfile)

while True:
    yaml_files = glob(os.path.join('messages', 'bot_servo*.yaml'))

    for yaml_file in yaml_files:
        process_servo_command(yaml_file)
        dest = os.path.join('store', f"ack_{os.path.basename(yaml_file)}")
        shutil.move(yaml_file, dest)

    time.sleep(1)
