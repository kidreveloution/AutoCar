import zmq
import time
import pygame
import sys

# Initialize Pygame and joystick
pygame.init()
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    sys.exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Initialized Joystick: {joystick.get_name()}")
print("Press joystick buttons or move axes. Press any button to exit.")

context = zmq.Context()
socket = context.socket(zmq.PUB)  # Create a publisher socket
socket.bind("tcp://*:5555")  # Bind on all interfaces on port 5555

while True:

    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axis = event.axis
            value = event.value
            if axis == 3:
                value = 0.05 * (value + 1) + 0.1
                value = format(float(value), ".2f")
                socket.send_string("steering,"+str(value))
                print(f"Axis {event.axis} moved to {value}")
            if axis == 1:
                value = (value * 100)

                if value >= -1 and value <= 1:
                    value = 0.00
                else:
                    value = format(float(value), ".2f")
                
                message = "power,"+str(value)

                socket.send_string("power,"+str(value))



