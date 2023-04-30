from time import sleep

from pitop import BrakingType, EncoderMotor, ForwardDirection

# Set the forward direction of each motor
motor_directions = {
    "M0": ForwardDirection.CLOCKWISE,
    "M1": ForwardDirection.CLOCKWISE,
    "M2": ForwardDirection.COUNTER_CLOCKWISE,
    "M3": ForwardDirection.COUNTER_CLOCKWISE
}

# Setup the motors
motors = {}
for motor_name, motor_direction in motor_directions.items():
    motor = EncoderMotor(motor_name, motor_direction)
    motor.braking_type = BrakingType.COAST
    motors[motor_name] = motor

# Gradually increase motor speed to 25 RPM
for i in range(1, 26):
    rpm_speed = i
    for motor in motors.values():
        motor.set_target_rpm(rpm_speed)
    sleep(0.1)

# Keep the motors running at 25 RPM for 5 seconds
sleep(5)

# Gradually decrease motor speed to 0 RPM
for i in range(25, 0, -1):
    rpm_speed = i
    for motor in motors.values():
        motor.set_target_rpm(rpm_speed)
    sleep(0.1)

# Stop the motors
for motor in motors.values():
    motor.set_target_rpm(0)
