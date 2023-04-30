# Pi-Top Zeta OmniBot

## File Structure
<code>
├── app.py
├── bot_move.py
├── bot_rotate.py
├── bot_sensors.py
├── bot_servo.py
├── bot_start.py
├── messages
│   ├── msg_bot_move_2023-04-30_01-00_001.yaml
│   ├── msg_bot_move_2023-04-30_01-23_001.yaml
│   ├── msg_bot_rotate_2023-04-30_09-20_001.yaml
│   └── msg_bot_ultrasonic_2023-04-30_09-22_001.yaml
├── __pycache__
│   ├── app.cpython-39.pyc
│   └── bot_start.cpython-39.pyc
├── store
│   ├── ack_bot_move_2023-04-30_01-00_001.yaml
│   ├── ack_bot_move_2023-04-30_01-23_001.yaml
│   ├── ack_bot_rotate_2023-04-30_09-20_001.yaml
│   └── ack_bot_ultrasonic_2023-04-30_09-22_001.yaml
└── templates
    └── index.html
</code>

## How it works

In principle, the functionality is very simple, you start the bot_start.py which starts all sub-processes. Including the 4 scripts for movement, rotation, servo and measurement. As soon as there is a YAML file with the required instructions in the "message" folder, it will be executed. Feedback is written to a msg_ file for further processing. The executed driving or moving command is moved to the "store" folder. Timestamps and consecutive numbers help to sort better.
