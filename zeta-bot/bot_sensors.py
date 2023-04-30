#!/usr/bin/env python3
import os
import time
import yaml
from pitop import UltrasonicSensor
from glob import glob
import shutil
from datetime import datetime

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def process_ultrasonic_command(filepath):
    ultrasonic_command = read_yaml_file(filepath)
    sensor_name = ultrasonic_command['sensor_name']

    distance_sensor = UltrasonicSensor(sensor_name, threshold_distance=0.2)
    distance = distance_sensor.distance

    write_ultrasonic_info_to_file(sensor_name, distance)

def write_ultrasonic_info_to_file(sensor_name, distance):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename_number = 1

    while True:
        filename_template = f"msg_bot_ultrasonic_{timestamp}_{filename_number:03d}.yaml"
        file_path = os.path.join('messages', filename_template)

        if not os.path.exists(file_path):
            break
        filename_number += 1

    ultrasonic_info = {
        "sensor_name": sensor_name,
        "distance": distance
    }

    with open(file_path, "w") as outfile:
        yaml.dump(ultrasonic_info, outfile)

while True:
    yaml_files = glob(os.path.join('messages', 'bot_ultrasonic*.yaml'))

    for yaml_file in yaml_files:
        process_ultrasonic_command(yaml_file)
        dest = os.path.join('store', f"ack_{os.path.basename(yaml_file)}")
        shutil.move(yaml_file, dest)

    time.sleep(1)
