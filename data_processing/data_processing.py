import threading
from confluent_kafka import Consumer, OFFSET_BEGINNING
import json
from producer import proceed_to_deliver
import os
from dotenv import load_dotenv

load_dotenv()

drone_id = os.getenv("DRONE_ID", default=0)

def processing_received(new_data: dict, details: dict):
    # дешифруем 
    if drone_id in new_data["deliver-to"] or new_data["deliver-to"] == "all":
        type = new_data['type']
        if type == "plane_data":
            details["operation"] = "plane_tasks"
        if type == "task_data":
            details["operation"] = "task_data"

def processing_departure(new_data: dict, details: dict):
    # шифруем 
    new_data["deliver_from"] = str(drone_id)
    # тут мы типа шифруем она большая функция да



#     "id": req_id,
#     "operation": "process_new_data",
#     "new_data": {
#         "type":"что за данные",
#         "deliver-from": "",
#         "deliver-to": "",
#         "data": { .... }
#         },
#     "component_to": "monitor"
#     }


def handle_event(id :str, details: dict):    
    # print(f"[debug] handling event {id}, {details}")
    print(f"[info] handling event {id}, {details['source']}->{details['deliver_to']}: {details['operation']}")
    
    # TODO: сделать остальные компоненты, а то в никуда передается по сути
    try:
        if details['operation'] == 'data_processing':
            new_data = details['new_data']            
            if details['deliver_from'] == "cooperation_tasks":
                processing_departure(new_data)
                details['new_data'] = new_data
                details['operation'] = 'data_outputting'
                details['deliver_to'] = 'connection'
                proceed_to_deliver(id, details)

                
            if details['deliver_from'] == "connection":
                processing_received(new_data, details)
                details['deliver_to'] = 'cooperation'
                proceed_to_deliver(id, details)

            
                
            
    except Exception as e:
        print(f"[error] failed to handle request: {e}")



def consumer_job(args, config):
    # Create Consumer instance
    monitor_consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(monitor_consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            monitor_consumer.assign(partitions)

    # Subscribe to topic
    topic = "monitor"
    monitor_consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = monitor_consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                # print("Waiting...")
                pass
            elif msg.error():
                print(f"[error] {msg.error()}")
            else:
                # Extract the (optional) key and value, and print.
                try:
                    id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    # print("[debug] consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    #     topic=msg.topic(), key=id, value=details_str))
                    handle_event(id, json.loads(details_str))
                except Exception as e:
                    print(
                        f"[error] malformed event received from topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        monitor_consumer.close()


def start_consumer(args, config):
    threading.Thread(target=lambda: consumer_job(args, config)).start()


if __name__ == '__main__':
    start_consumer(None)