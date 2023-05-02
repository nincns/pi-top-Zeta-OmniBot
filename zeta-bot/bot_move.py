#!/usr/bin/env python3
#content of bot_move.py
import os
import time
import yaml
from pitop import BrakingType, EncoderMotor, ForwardDirection
from glob import glob
import shutil
from datetime import datetime

def check_kill_switch(kill_switch_file="messages/kill_switch.yaml"):
    return os.path.exists(kill_switch_file)

def process_file(filepath):
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)

    motors = [motor_fl, motor_bl, motor_fr, motor_br]

    initial_distances = {motor: motor.distance for motor in motors}

    for motor in motors:
        motor.set_target_rpm(config['rpm'])

    while abs(motor_fl.distance - initial_distances[motor_fl]) < config['distance']:
        pass

    for motor in motors:
        motor.stop()

    write_motor_distances_to_file(motors, initial_distances)

def write_motor_distances_to_file(motors, initial_distances):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename_number = 1

    while True:
        filename_template = f"msg_bot_move_{timestamp}_{filename_number:03d}.yaml"
        file_path = os.path.join("messages", filename_template)

        if not os.path.exists(file_path):
            break
        filename_number += 1

    motor_distances = {motor.name: round(motor.distance - initial_distances[motor], 2) for motor in motors}
    with open(file_path, "w") as outfile:
        yaml.dump(motor_distances, outfile)

def calibrate_motors(motors):
    for motor in motors:
        motor.set_target_rpm(10)
        while motor.distance == 0:
            pass
        motor.stop()

def check_for_files(prefixes, directory="messages"):
    files = os.listdir(directory)
    for prefix in prefixes:
        for file in files:
            if file.startswith(prefix):
                return True
    return False

def sort_files_by_creation_time(files):
    return sorted(files, key=os.path.getctime)

def get_sorted_move_and_rotate_files():
    move_files = glob("messages/bot_move*.yaml")
    rotate_files = glob("messages/bot_rotate*.yaml")
    all_files = move_files + rotate_files
    return sort_files_by_creation_time(all_files)

motor_fl = EncoderMotor(port_name="M0", name="motor_fl", forward_direction=ForwardDirection.CLOCKWISE)
motor_bl = EncoderMotor(port_name="M1", name="motor_bl", forward_direction=ForwardDirection.CLOCKWISE)
motor_fr = EncoderMotor(port_name="M2", name="motor_fr", forward_direction=ForwardDirection.COUNTER_CLOCKWISE)
motor_br = EncoderMotor(port_name="M3", name="motor_br", forward_direction=ForwardDirection.COUNTER_CLOCKWISE)

motors = [motor_fl, motor_bl, motor_fr, motor_br]

for motor in motors:
    motor.wheel_diameter = 6.1
    motor.braking_type = BrakingType.COAST

calibrate_motors(motors)

while True:
    if check_kill_switch():
        for motor in motors:
            motor.stop()
        print("Kill switch detected. Stopping all motors and exiting.")
        break
    if not check_for_files(["progress_bot_move", "progress_bot_rotate"]):
        sorted_files = get_sorted_move_and_rotate_files()
        for file in sorted_files:
            if "bot_rotate" in file:
                # Wait for the bot_rotate file to be removed
                while os.path.exists(file):
                    time.sleep(1)
                continue
            elif "bot_move" in file:
                prefix = "bot_move"
            else:
                continue

            new_filename = file.replace(prefix, f"progress_{prefix}")
            os.rename(file, new_filename)
            process_file(new_filename)
            ack_filename = os.path.join("store", f"ack_{os.path.basename(new_filename)}")
            os.rename(new_filename, ack_filename)
    time.sleep(1)
