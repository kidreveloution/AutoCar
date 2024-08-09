import zmq
import requests
import json
import time
import random

# Message class
class MESSAGE_CLASS:
    def __init__(self, address: str, msg_name: str, dest: str, content: dict):
        """
        Initializes the message builder with the necessary attributes.

        Args:
            address (str): The address of the sender.
            msg_name (str): The name of the message.
            dest (str): The destination address of the message.
            content (dict): The content of the message, as a dictionary.
        """
        self.address = address
        self.msg_name = msg_name
        self.dest = dest
        self.content = content
    
    def buildMessage(self) -> str:
        """
        Builds the message as a JSON string.

        Returns:
            str: The JSON-encoded message.
        """
        message = {
            'address': self.address,
            'dest': self.dest,
            'msg_name': self.msg_name,
            'content': self.content
        }
        return json.dumps(message)

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

# Get fake public IP
def get_fake_public_ip():
    return "192.168.1.100"  # Fake IP address

# Setup ZeroMQ
SERVER_IP = '3.22.90.156'
WORKER_ID = "fake_car_1"
PUBLIC_IP = get_fake_public_ip()

context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect("tcp://"+SERVER_IP+":5555")

# Send initial fake message with work ID and current IP address
initial_message = MESSAGE_CLASS(
    address=WORKER_ID,
    msg_name="initial_connection",
    dest=SERVER_IP,
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
        gps_message = MESSAGE_CLASS(
            address=WORKER_ID,
            msg_name="gps_update",
            dest=SERVER_IP,
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
