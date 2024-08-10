import zmq
import json

context = zmq.Context()

# Router socket for routing messages based on tx_id
router = context.socket(zmq.ROUTER)
router.bind("tcp://*:5555")

connections = {}

while True:
    message = router.recv_multipart()
    print(f"Received raw message: {message}")
    # Decode each part of the multipart message as UTF-8
    
    tx_id = message[1].decode('utf-8')

    message_content = message[2].decode('utf-8')  # Decode the message content as UTF-8
    message_data = json.loads(message_content)

    rx_id = message_data["rx_id"]

    print(message_data)
    if message_data.get("msg_name") == "registeration":
        # Register the worker with its decoded ID and IP addresscd 
        ip_address = message_data["content"]["ip_address"]

        print(f"Decoded tx_id: {tx_id}, IP: {ip_address}, Content: {message_content}")
        connections[tx_id] = ip_address
        content = b"YOU HAVE BEEN REGISTERED"
        router.send_multipart([tx_id.encode('utf-8'), content])  # Encode the response back to UTF-8
        print(f"Registered worker: {tx_id} with IP: {ip_address}")
    else:
        if tx_id in connections:
            content = message_content.encode('utf-8')
            router.send_multipart([rx_id.encode('utf-8'), content])  # Encode the response back to UTF-8
            print(f"Sent message to reciever {rx_id}")
        else:
            print(f"TX ID {tx_id} not recognized.")

    print(f"Current connections: {connections}")
