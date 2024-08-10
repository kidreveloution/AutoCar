import zmq
import requests
import json
import time
import random
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import common.messageBuilder as messageBuilder


# Generate fake GPS coordinates
def generate_fake_gps():
    # Randomly generate coordinates near a specific point
    base_lat = 42.2808  # Base latitude (e.g., near Ann Arbor, MI)
    base_lon = -83.7430  # Base longitude

    lat_variation = random.uniform(-0.01, 0.01)
    lon_variation = random.uniform(-0.01, 0.01)

    return {
        "latitude": base_lat + lat_variation,
        "longitude": base_lon + lon_variation
    }

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

# Setup ZeroMQ
SERVER_IP = '3.22.90.156'
tx_id = "fake_car_1"
PUBLIC_IP = get_public_ip()

context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect("tcp://"+SERVER_IP+":5555")

# Send initial fake message with work ID and current IP address
initial_message = messageBuilder.MESSAGE_CLASS(
    tx_id=tx_id,
    msg_name="registeration",
    rx_id="mother",
    content={"ip_address": PUBLIC_IP}
).buildMessage()


dealer.send_multipart([PUBLIC_IP.encode('utf-8'), initial_message.encode('utf-8')])

try:
    print("Trying")
    while True:
        # Receive and process incoming messages
        # message = dealer.recv_multipart()
        # if isinstance(message, list) and len(message) > 0 and isinstance(message[0], bytes):
        #     message = message[0].decode('utf-8')
        # else:
        #     message = message.decode('utf-8')
    
        # message = json.loads(message)
        # command = message['msg_name']
        # val = message['content']

        #print(command, val)

        # Send periodic fake GPS data
        fake_gps_data = generate_fake_gps()
        gps_message = messageBuilder.MESSAGE_CLASS(
            tx_id=tx_id,
            msg_name="gps_update",
            rx_id="mother",
            content=fake_gps_data
        ).buildMessage()
        print("SENDING MEssAGE")
        dealer.send_multipart([PUBLIC_IP.encode('utf-8'), gps_message.encode('utf-8')])

        time.sleep(5)  # Adjust the sleep interval as needed
except KeyboardInterrupt:
    print("Stopping...")

except Exception as e:
    print("ERROR")

    print("An error occurred:", str(e))
