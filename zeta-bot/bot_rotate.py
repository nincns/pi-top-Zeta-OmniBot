#!/usr/bin/env python3
#content of bot_rotate.py
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

    motors = {
        'direction_fl': motor_fl,
        'direction_bl': motor_bl,
        'direction_fr': motor_fr,
        'direction_br': motor_br
    }

    active_motors = []
    initial_rotations = {}

    for direction_key, direction in config.items():
        if direction_key.startswith('direction_'):
            motor = motors.get(direction_key)
            if motor:
                motor.set_target_rpm(config['rpm'] if direction == "CW" else -config['rpm'])
                active_motors.append(motor)
                initial_rotations[motor] = motor.rotation_counter

    while active_motors:
        for motor in active_motors:
            if abs(motor.rotation_counter - initial_rotations[motor]) >= config['target_rotation']:
                motor.stop()
                active_motors.remove(motor)

    write_rotation_to_file(config, config['target_rotation'])

def write_rotation_to_file(config, target_rotation):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename_number = 1

    while True:
        filename_template = f"msg_bot_rotate_{timestamp}_{filename_number:03d}.yaml"
        file_path = os.path.join("messages", filename_template)

        if not os.path.exists(file_path):
            break
        filename_number += 1

    left_motors_cw = config.get('direction_fl') == "CW" and config.get('direction_bl') == "CW"
    right_motors_cw = config.get('direction_fr') == "CW" and config.get('direction_br') == "CW"

    rotation_angle = (target_rotation / 1.35) * 180
    rotation_direction = "right" if left_motors_cw and right_motors_cw else "left"

    rotation_info = {
        "rotation_angle": round(rotation_angle, 2),
        "rotation_direction": rotation_direction
    }

    with open(file_path, "w") as outfile:
        yaml.dump(rotation_info, outfile)

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
motor_fr = EncoderMotor(port_name="M2", name="motor_fr", forward_direction=ForwardDirection.CLOCKWISE)
motor_br = EncoderMotor(port_name="M3", name="motor_br", forward_direction=ForwardDirection.CLOCKWISE)

motors = [motor_fl, motor_bl, motor_fr, motor_br]

for motor in motors:
    motor.wheel_diameter = 6.1
    motor.braking_type = BrakingType.COAST

while True:
    if check_kill_switch():
        for motor in motors:
            motor.stop()
        print("Kill switch detected. Stopping all motors and exiting.")
        break
    if not check_for_files(["progress_bot_move", "progress_bot_rotate"]):
        sorted_files = get_sorted_move_and_rotate_files()
        waiting_for_bot_move = False
        
        for i, file in enumerate(sorted_files):
            if "bot_move" in file:
                if i == 0:  # Die bot_move-Datei ist die nächste in der zeitlichen Reihenfolge
                    waiting_for_bot_move = True
                    break
                else:
                    continue
            elif "bot_rotate" in file:
                prefix = "bot_rotate"
            else:
                continue

            if not waiting_for_bot_move:
                new_filename = file.replace(prefix, f"progress_{prefix}")
                os.rename(file, new_filename)
                process_file(new_filename)
                ack_filename = os.path.join("store", f"ack_{os.path.basename(new_filename)}")
                os.rename(new_filename, ack_filename)
            else:
                break
    time.sleep(1)
