# Pi-Top Zeta OmniBot

## File Structure
<code>
├── S0.txt
├── S7.txt
├── __pycache__
│   ├── app.cpython-39.pyc
│   └── camera.cpython-39.pyc
├── app.py
├── bot_move.py
├── bot_rotate.py
├── bot_sensors.py
├── bot_servo.py
├── bot_start.py
├── camera.py
├── drive_scripts
│   ├── delete-queues.sh
│   ├── drive-around-left.sh
│   ├── drive-around-right.sh
│   ├── drive-past-left.sh
│   ├── drive-past-right.sh
│   ├── get-slower.sh
│   ├── getting-faster.sh
│   ├── left-on-the-way.sh
│   ├── move-back.sh
│   ├── move-forward.sh
│   ├── right-on-th-way.sh
│   ├── rotate-left.sh
│   ├── rotate-right.sh
│   ├── servo-left-back.sh
│   ├── servo-left-forward.sh
│   ├── slide-left-back.sh
│   ├── slide-left-forward.sh
│   ├── slide-left.sh
│   ├── slide-right-back.sh
│   ├── slide-right-forward.sh
│   ├── slide-right.sh
│   ├── stop-all.sh
│   └── template_rotation.sh
├── messages
├── rotation.conf
├── speed.conf
├── static
│   └── images
│       ├── buttons
│       │   ├── 1.png - 28.png
│       ├── mecanum_wheels.png
│       └── not_found.jpeg
├── store
└── templates
    └── index.html
</code>

## How it works

In principle, the functionality is very simple, you start the bot_start.py which starts all sub-processes. Including the 4 scripts for movement, rotation, servo and measurement. As soon as there is a YAML file with the required instructions in the "message" folder, it will be executed. Feedback is written to a msg_ file for further processing. The executed driving or moving command is moved to the "store" folder. Timestamps and consecutive numbers help to sort better.

## how to start

Start the bot_start.py with sudo or better than root
<code>
python3 bot_start.py
</code>
The web server is reachable under the IP of the host with port 5000 ex. http://< ip-address >:5000

## Flask Application server (server)

Parallel to the 4 function scripts, the web server is also started, which presents the possible inputs as a web form. When entering the values, they are processed as well as in the console program, files are generated and the robot is moved.

## Initial process:

At the beginning, the wheels are briefly rotated to turn all to the same measuring mark. Although only one wheel is used as a reference, it would not be necessary if you accept slight deviations in the distance. But it looks nicer if all 4 return values of the wheels are identical.

## Note on the simple robotic kit

In principle, the program can already be used with the simple robotic kit, because all requirements are already met with the take-away roller and the normal wheels. However, the wheels are slightly larger (75mm) and this would have to be adjusted.
At the beginning, the wheels are briefly rotated to turn all to the same measuring mark. Although only one wheel is used as a reference, it would not be necessary if you accept slight deviations in the distance. But it looks nicer if all 4 return values of the wheels are identical.
At the beginning, the wheels are briefly rotated to turn all to the same measuring mark. Although only one wheel is used as a reference, it would not be necessary if you accept slight deviations in the distance. But it looks nicer if all 4 return values of the wheels are identical.

## Last Changes

All current functions are running perfectly, I have also prepared an emergency stop.
