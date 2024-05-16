
import multiprocessing
import threading
from confluent_kafka import Producer
import json
import random
import time

_requests_queue: multiprocessing.Queue = None

def gps_data():
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    count = 1
    while True:
        if count % 3 == 0:
            latitude += random.uniform(1, 10)
            longitude += random.uniform(1, 10)
        if count % 3 != 0:
            latitude -= random.uniform(1, 10)
            longitude -= random.uniform(1, 10)
        time.time(5)
        data = {
            "deliver-to": "navigation",
            "operation": "gps_location_data",
            "data_location": {
                "latitude": str(latitude) , 
                "longitude": str(longitude)
            }

        }
        proceed_to_deliver(data)
    

def proceed_to_deliver(details):
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
        event_details['source'] = 'gps'
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
    
if __name__ == '__main__':
    start_producer(None, None, None)
    gps_data()