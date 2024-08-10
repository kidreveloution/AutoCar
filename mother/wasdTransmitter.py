import zmq
import keyboard
import sys
import time
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader
# Set up ZMQ

# Initial values
power = 0.00
steering = 0.15
power_step = 5.00  # Amount to increase/decrease per step
steering_step = 0.01  # Amount to increase/decrease per step


zmq_inst = zmqHeader.ZMQ_CONNECTION(
    TX_ID="MOTHER",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=None
)

print(zmq_inst.connectZMQ())

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
