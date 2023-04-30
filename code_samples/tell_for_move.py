from time import sleep

from pitop import BrakingType, EncoderMotor, ForwardDirection

# Prompt user to choose motor directions
motor_directions = {}
while True:
    direction = input("Choose motor direction for M0 (cw for clockwise, ccw for counter-clockwise): ")
    if direction.lower() == "cw":
        motor_directions["M0"] = ForwardDirection.CLOCKWISE
        break
    elif direction.lower() == "ccw":
        motor_directions["M0"] = ForwardDirection.COUNTER_CLOCKWISE
        break
    else:
        print("Invalid input. Please enter 'cw' or 'ccw'.")

while True:
    direction = input("Choose motor direction for M1 (cw for clockwise, ccw for counter-clockwise): ")
    if direction.lower() == "cw":
        motor_directions["M1"] = ForwardDirection.CLOCKWISE
        break
    elif direction.lower() == "ccw":
        motor_directions["M1"] = ForwardDirection.COUNTER_CLOCKWISE
        break
    else:
        print("Invalid input. Please enter 'cw' or 'ccw'.")

while True:
    direction = input("Choose motor direction for M2 (cw for clockwise, ccw for counter-clockwise): ")
    if direction.lower() == "cw":
        motor_directions["M2"] = ForwardDirection.CLOCKWISE
        break
    elif direction.lower() == "ccw":
        motor_directions["M2"] = ForwardDirection.COUNTER_CLOCKWISE
        break
    else:
        print("Invalid input. Please enter 'cw' or 'ccw'.")

while True:
    direction = input("Choose motor direction for M3 (cw for clockwise, ccw for counter-clockwise): ")
    if direction.lower() == "cw":
        motor_directions["M3"] = ForwardDirection.CLOCKWISE
        break
    elif direction.lower() == "ccw":
        motor_directions["M3"] = ForwardDirection.COUNTER_CLOCKWISE
        break
    else:
        print("Invalid input. Please enter 'cw' or 'ccw'.")

# Prompt user to enter motor speed and runtime
while True:
    try:
        rpm_speed = int(input("Enter motor speed (in RPM): "))
        runtime = int(input("Enter runtime (in seconds): "))
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

# Setup the motors
motors = {}
for motor_name, motor_direction in motor_directions.items():
    motor = EncoderMotor(motor_name, motor_direction)
    motor.braking_type = BrakingType.COAST
    motors[motor_name] = motor

# Set the RPM speed for all motors
for motor in motors.values():
    motor.set_target_rpm(rpm_speed)

# Keep the motors running at the same speed for the specified runtime
sleep(runtime)

# Gradually decrease motor speed to 0 RPM
for i in range(rpm_speed, 0, -1):
    for motor in motors.values():
        motor.set_target_rpm(i)
    sleep(0.1)

# Stop the motors
for motor in motors.values():
    motor.set_target_rpm(0)
