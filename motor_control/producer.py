
import multiprocessing
import threading
from confluent_kafka import Producer
import json
from uuid import uuid4
import random
import time

_requests_queue: multiprocessing.Queue = None

def proceed_to_deliver(id, details):
    # print(f"[debug] queueing for delivery event id: {id}, payload: {details}")    
    _requests_queue.put(details)


def producer_job(_, config, requests_queue: multiprocessing.Queue):
    

    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('[error] Message failed delivery: {}'.format(err))

    # Produce data by selecting random values from these lists.
    topic = "monitor"

    while True:
        event_details = requests_queue.get()
        event_details['source'] = 'motor_control'
        producer.produce(topic, json.dumps(event_details), event_details['id'],  
            callback=delivery_callback
        )
        # Block until the messages are sent.
        producer.poll(10000)
        producer.flush()

def start_producer(args, config, requests_queue):
    global _requests_queue
    _requests_queue = requests_queue
    threading.Thread(target=lambda: producer_job(args, config, requests_queue)).start()
    
# def motor_status(value):
#     req_id = uuid4().__str__()
#     details = {
#         "id": req_id,
#         "operation": "battery_status",
#         "new_data": str(value),
#         "deliver_to": "technical_data"
#     }
#     proceed_to_deliver(req_id, details)

def motor_status_simulation():
    while True:
        time.sleep(10)
        # check = True
        # if check:
        data = {
            "deliver-to": "technical_data",
            "operation": "motor_status",
            "status": "OK" 
        }
    

if __name__ == '__main__':
    start_producer(None, None, None)
    motor_status_simulation()