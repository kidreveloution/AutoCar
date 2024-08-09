import zmq
import json

context = zmq.Context()

# Router socket for routing messages based on worker_id
router = context.socket(zmq.ROUTER)
router.bind("tcp://*:5555")

workers = {}

while True:
    message = router.recv_multipart()
    message = json.loads(message)

    if message["msg_name"] == "registeration":
        worker_id = message["address"]
        ip_address = message["ip_address"]
        content = b"YOU HAVE BEEN REGISTERED"
        router.send_multipart([worker_id.encode('utf-8'),content])
        workers[worker_id] = ip_address
        continue
    if worker_id in workers:
        router.send_multipart([workers[worker_id], content])
    else:
        print(f"Worker ID {worker_id} not recognized.")
   
    print(message)
