#!/usr/bin/env python3
import os
import signal
import yaml
from datetime import datetime
import subprocess
import sys
import threading
import time
import atexit
from flask import Flask
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def signal_handler(sig, frame):
    print("\nStopping Flask server...")
    flask_server.terminate()
    print("Stopped Flask server.")
    
    print("Stopping TensorFlow Serving ImageClassifier server...")
    tf_ic_server.terminate()
    print("Stopped TensorFlow Serving ImageClassifier server.")
    
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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

def set_movement():
    rpm = int(input("Enter RPM (-114 to 114): "))
    distance = float(input("Enter distance in cm: "))

    data = {
        "rpm": rpm,
        "distance": distance
    }

    write_config_to_file("bot_move", data)

def set_rotation():
    rpm = int(input("Enter RPM (-114 to 114): "))
    direction_fl = input("Enter direction for M0 (CW or CCW): ")
    direction_bl = input("Enter direction for M1 (CW or CCW): ")
    direction_fr = input("Enter direction for M2 (CW or CCW): ")
    direction_br = input("Enter direction for M3 (CW or CCW): ")
    target_rotation = float(input("Enter number of wheel rotations: "))

    data = {
        "rpm": rpm,
        "direction_fl": direction_fl,
        "direction_bl": direction_bl,
        "direction_fr": direction_fr,
        "direction_br": direction_br,
        "target_rotation": target_rotation
    }

    write_config_to_file("bot_rotate", data)

def set_servo_position():
    servo_name = input("Enter servo name (S0 or S3): ")
    angle = int(input("Enter angle (-90 to 90): "))

    data = {
        "servo_name": servo_name,
        "angle": angle
    }

    write_config_to_file("bot_servo", data)

def get_measurement():
    sensor_name = input("Enter sensor name (D0 or D7): ")

    data = {
        "sensor_name": sensor_name
    }

    write_config_to_file("bot_ultrasonic", data)

def start_subprocess(script_name):
    return subprocess.Popen(["python3", script_name])

class MessageEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".yaml") and "msg_bot_" in event.src_path:

            with open(event.src_path, "r") as file:
                content = file.read()
                print(f"\nNew message in {event.src_path}:\n{content}\n")

def main():
    try:
        move_process = subprocess.Popen(["python3", "bot_move.py"])
        rotate_process = subprocess.Popen(["python3", "bot_rotate.py"])
        servo_process = subprocess.Popen(["python3", "bot_servo.py"])
        sensors_process = subprocess.Popen(["python3", "bot_sensors.py"])
        flask_process = subprocess.Popen(["export FLASK_APP=app.py && export FLASK_ENV=development && flask run --host=0.0.0.0 --port=5000"],
                                 stdout=subprocess.DEVNULL,
                                 shell=True,
                                 preexec_fn=os.setsid)
        print("Started Flask server!")

        print("Subprocesses started successfully.")
    except Exception as e:
        print("Error starting subprocesses:", e)
        sys.exit(1)

    observer = Observer()
    event_handler = MessageEventHandler()
    observer.schedule(event_handler, "messages", recursive=False)
    observer.start()

    while True:
        print("1. set movement")
        print("2. set rotation")
        print("3. set servo position")
        print("4. get measurement")
        print("5. quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            set_movement()
        elif choice == "2":
            set_rotation()
        elif choice == "3":
            set_servo_position()
        elif choice == "4":
            get_measurement()
        elif choice == "5":
            move_process.terminate()
            rotate_process.terminate()
            servo_process.terminate()
            sensors_process.terminate()
            flask_process.terminate()
            observer.stop()
            observer.join()
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
