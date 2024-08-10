import zmq
import keyboard
import sys
import time
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import common.messageBuilder as messageBuilder

# Set up ZMQ
context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect("tcp://3.22.90.156:5555")
CLIENT_ID = "mother"
target_worker_id = "car_1"

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

initial_message = messageBuilder.MESSAGE_CLASS(
    tx_id=CLIENT_ID,
    msg_name="registeration",
    rx_id="router",
    content={"ip_address": get_public_ip()}
).buildMessage()


dealer.send_multipart([CLIENT_ID.encode('utf-8'), initial_message.encode('utf-8')])

# Initial values
power = 0.00
steering = 0.15
power_step = 5.00  # Amount to increase/decrease per step
steering_step = 0.01  # Amount to increase/decrease per step

# Define a function to send messages
def send_message(msg_name, value):
    message = messageBuilder.MESSAGE_CLASS(
        address=CLIENT_ID,
        msg_name=msg_name,
        dest=target_worker_id,
        content=format(float(value), ".2f")
    )
    dealer.send_multipart([message.dest.encode('utf-8'), message.buildMessage().encode('utf-8')])
    print(f"Sent {msg_name}: {value}")

# # Main loop
# try:
#     while True:
#         if keyboard.is_pressed('w'):
#             power = min(100.00, power + power_step)  # Increase power, max 100
#             send_message("power", power)
#         elif keyboard.is_pressed('s'):
#             power = max(-100.00, power - power_step)  # Decrease power, min -100
#             send_message("power", power)
#         else:
#             power = 0.00  # Stop power when neither W nor S is pressed
#             send_message("power", power)

#         if keyboard.is_pressed('a'):
#             steering = max(0.10, steering - steering_step)  # Decrease steering, min 0.10
#             send_message("steering", steering)
#         elif keyboard.is_pressed('d'):
#             steering = min(0.20, steering + steering_step)  # Increase steering, max 0.20
#             send_message("steering", steering)
#         else:
#             steering = 0.15  # Reset steering to default when neither A nor D is pressed
#             send_message("steering", steering)

#         time.sleep(0.1)  # Small delay to control the rate of change

# except KeyboardInterrupt:
#     print("Program interrupted")
#     sys.exit()
