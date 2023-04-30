#!/usr/bin/env python3
import os
import time
import yaml
from pitop import BrakingType, EncoderMotor, ForwardDirection
from glob import glob
import shutil
from datetime import datetime

def process_file(filepath):
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)

    motors = [motor_fl, motor_bl, motor_fr, motor_br]
    directions = [config['direction_fl'], config['direction_bl'], config['direction_fr'], config['direction_br']]

    for motor, direction in zip(motors, directions):
        motor.set_target_rpm(config['rpm'] if direction == "CW" else -config['rpm'])

    initial_rotation = motor_fl.rotation_counter

    while abs(motor_fl.rotation_counter - initial_rotation) < config['target_rotation']:
        pass

    for motor in motors:
        motor.stop()

    write_rotation_to_file(directions, config['target_rotation'])

def write_rotation_to_file(directions, target_rotation):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    filename_number = 1

    while True:
        filename_template = f"msg_bot_rotate_{timestamp}_{filename_number:03d}.yaml"
        file_path = os.path.join("messages", filename_template)

        if not os.path.exists(file_path):
            break
        filename_number += 1

    left_motors_cw = directions[0] == "CW" and directions[1] == "CW"
    right_motors_cw = directions[2] == "CW" and directions[3] == "CW"

    rotation_angle = (target_rotation / 1.35) * 180
    rotation_direction = "right" if left_motors_cw and right_motors_cw else "left"

    rotation_info = {
        "rotation_angle": round(rotation_angle, 2),
        "rotation_direction": rotation_direction
    }

    with open(file_path, "w") as outfile:
        yaml.dump(rotation_info, outfile)

motor_fl = EncoderMotor(port_name="M0", name="motor_fl", forward_direction=ForwardDirection.CLOCKWISE)
motor_bl = EncoderMotor(port_name="M1", name="motor_bl", forward_direction=ForwardDirection.CLOCKWISE)
motor_fr = EncoderMotor(port_name="M2", name="motor_fr", forward_direction=ForwardDirection.CLOCKWISE)
motor_br = EncoderMotor(port_name="M3", name="motor_br", forward_direction=ForwardDirection.CLOCKWISE)

motors = [motor_fl, motor_bl, motor_fr, motor_br]

for motor in motors:
    motor.wheel_diameter = 6.1
    motor.braking_type = BrakingType.COAST

while True:
    files = glob("messages/bot_rotate*.yaml")
    for file in files:
        process_file(file)
        dest = os.path.join("store", f"ack_{os.path.basename(file)}")
        shutil.move(file, dest)
    time.sleep(1)
