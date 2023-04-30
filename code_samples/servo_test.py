from time import sleep
from pitop import ServoMotor, ServoMotorSetting

# Ask the user for the servo name
servo_name = input("Please enter the servo name (e.g. 'S0'): ")

# Initialize the servo motor object with the specified name
servo = ServoMotor(servo_name)

# Run an infinite loop to keep asking the user for input until they exit
while True:
    # Ask the user for input (angle or "exit" to quit)
    angle = input("Please enter the desired angle (-90 to 90), or 'exit' to quit: ")

    # If the user entered "exit", break out of the loop to quit the program
    if angle.lower() == "exit":
        break

    try:
        # Attempt to convert the user's input to an integer angle value
        angle = int(angle)
        
        # If the angle value is within the acceptable range, set the servo's target angle
        if -90 <= angle <= 90:
            servo.target_angle = angle
        else:
            print("Invalid angle. Please enter an angle between -90 and 90 degrees.")
    except ValueError:
        # If the user's input was not a valid integer, print an error message and continue the loop
        print("Invalid input. Please enter a number or 'exit'.")
        continue

# Print a message to indicate that the program has ended
print("Program terminated.")