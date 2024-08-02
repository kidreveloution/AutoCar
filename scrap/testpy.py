import zmq
import time
import keyboard  # You need to install this module using `pip install keyboard`
import sys

# Initialize ZMQ
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

steering_value = 0.55  # Initial steering value
power_value = 0.0  # Initial power value

print("Press W, A, S, D keys to control. Press ESC to exit.")

try:
    while True:
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break

        if keyboard.is_pressed('w'):
            power_value = 100.0
        elif keyboard.is_pressed('s'):
            power_value = -100.0
        else:
            power_value = 0.0

        if keyboard.is_pressed('a'):
            steering_value = 0.10
        elif keyboard.is_pressed('d'):
            steering_value = 1.00
        else:
            steering_value = 0.55

        # Format the values
        formatted_steering_value = format(float(steering_value), ".2f")
        formatted_power_value = format(float(power_value), ".2f")

        # Send steering value
        socket.send_string("steering," + formatted_steering_value)
        print(f"Steering moved to {formatted_steering_value}")

        # Send power value
        socket.send_string("power," + formatted_power_value)
        print(f"Power moved to {formatted_power_value}")

        # Add a delay to avoid flooding the network
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    socket.close()
    context.term()
    print("ZMQ context closed")
