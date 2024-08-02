import zmq

context = zmq.Context()

# Router socket for routing messages based on worker_id
router = context.socket(zmq.ROUTER)
router.bind("tcp://*:5555")

workers = {}

while True:
    message = router.recv_multipart()
    identity, worker_id, content = message
    worker_id = worker_id.decode('utf-8')
    print(message)
    if content == b"":  # Registration message
        print("REGISTERING ", worker_id)
        content = b"YOU HAVE BEEN REGISTERED"
        router.send_multipart([worker_id.encode('utf-8'),content])
        workers[worker_id] = identity
        continue
    
    if worker_id in workers:
        router.send_multipart([workers[worker_id], content])
    else:
        print(f"Worker ID {worker_id} not recognized.")

