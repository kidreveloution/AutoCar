import requests
import sys
import zmq
import time
sys.path.append('/Users/alyeldinshahin/Documents/GitHub/AutoCar')
import messageBuilder

context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect("tcp://3.22.90.156:5555")

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

address = get_public_ip()
msg_name = "steering"
dest = "car_1"
content = 5

message = messageBuilder.MESSAGE_CLASS(
    address=address,
    msg_name=msg_name,
    dest=dest,
    content=content
    )



while True:
    time.sleep(3)
    dealer.send_multipart([message.dest.encode('utf-8'), message.buildMessage().encode('utf-8')])
    print("Message Sent")


