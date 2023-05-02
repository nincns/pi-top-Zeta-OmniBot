# Pi-Top Zeta OmniBot

## File Structure
<code>
├── app.py
├── bot_move.py
├── bot_rotate.py
├── bot_sensors.py
├── bot_servo.py
├── bot_start.py
├── camera.py
├── images
│   └── not_found.jpeg
├── messages
│   ├── kill.sh
│   ├── move.sh
│   └── rotate.sh
├── __pycache__
│   ├── app.cpython-39.pyc
│   └── camera.cpython-39.pyc
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
The web server is reachable under the IP of the host with port 5000 ex. http://<ip-address>:5000

## Flask Application server (server)

Parallel to the 4 function scripts, the web server is also started, which presents the possible inputs as a web form. When entering the values, they are processed as well as in the console program, files are generated and the robot is moved.

## Initial process:

At the beginning, the wheels are briefly rotated to turn all to the same measuring mark. Although only one wheel is used as a reference, it would not be necessary if you accept slight deviations in the distance. But it looks nicer if all 4 return values of the wheels are identical.

## Note on the simple robotic kit

In principle, the program can already be used with the simple robotic kit, because all requirements are already met with the take-away roller and the normal wheels. However, the wheels are slightly larger (75mm) and this would have to be adjusted.
At the beginning, the wheels are briefly rotated to turn all to the same measuring mark. Although only one wheel is used as a reference, it would not be necessary if you accept slight deviations in the distance. But it looks nicer if all 4 return values of the wheels are identical.
At the beginning, the wheels are briefly rotated to turn all to the same measuring mark. Although only one wheel is used as a reference, it would not be necessary if you accept slight deviations in the distance. But it looks nicer if all 4 return values of the wheels are identical.

## Last Changes

alle aktuellen Funktionen laufen einwandfrei, ich habe zusätzlich einen Notstop vorbereitet.
