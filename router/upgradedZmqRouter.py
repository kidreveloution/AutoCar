import zmq
import json

context = zmq.Context()

# Router socket for routing messages based on worker_id
router = context.socket(zmq.ROUTER)
router.bind("tcp://*:5555")

workers = {}

while True:
    message = router.recv_multipart()
    print(f"Received raw message: {message}")

    # The first part of the message is the worker_id, treat it as binary
    worker_id = message[0]
    
    # Decode the remaining parts as UTF-8
    ip_address = message[1].decode('utf-8')
    message_content = message[2].decode('utf-8')

    print(f"Worker ID (binary): {worker_id}, IP: {ip_address}, Content: {message_content}")

    message_data = json.loads(message_content)

    if message_data.get("msg_name") == "registeration":
        # Register the worker with its binary ID and IP address
        workers[worker_id] = ip_address
        content = b"YOU HAVE BEEN REGISTERED"
        router.send_multipart([worker_id, content])
        print(f"Registered worker: {worker_id} with IP: {ip_address}")
    else:
        if worker_id in workers:
            content = message_content.encode('utf-8')
            router.send_multipart([worker_id, content])
            print(f"Sent message to worker {worker_id}")
        else:
            print(f"Worker ID {worker_id} not recognized.")

    print(f"Current workers: {workers}")
