import threading
from confluent_kafka import Consumer, OFFSET_BEGINNING
import json
from producer import proceed_to_deliver

# glob_final_data = []
final_data = {
    "deliver_to": "data_processing",
    "operation": "three_in_one",
    "new-data": {
        "task-data":"",
        "detection-data":""
    }
}
def handle_event(id, details):    
    # print(f"[debug] handling event {id}, {details}")
    print(f"[info] handling event {id}, {details['source']}->{details['deliver_to']}: {details['operation']}")
    # global glob_final_data
    global final_data
    try:
        if details["source"] == "data_processing":
            print("Выбирается подзадание и полетное задание отправляется в coop_plane")
            # if details["operation"] == "task_plane_data":
            final_data["new-data"]["task-data"] = details["new-data"]["task-data"]
            details["deliver_to"] = "cooperation_plane"
            details['operation'] = 'plane_data'
            proceed_to_deliver(id, details)
        
        if details["source"] == "detector_control":
            if details["operation"] == 'detection_data':
                print("Данные об обнаружении человека")
                final_data["id"] = details["id"]
                final_data["new-data"]["detection-data"] = details["new-data"]
                proceed_to_deliver(id, final_data)


            
            
            
        
        # if details["source"] == "detector-control":
        #     print("Data of detection => this data is sending to data_processing")
        #     details["deliver_to"] = "data_processing"
        #     details['operation'] = 'detection_data'
        #     # glob_final_data.append(details)
        #     # proceed_to_deliver(id, details)
        # if details["source"] == "cooperation_plane":
        #     print("Data of coordinates => coordinates is sent to data_processing")
        #     final_data["task-data"] = details["new_data"]["task-data"]
        #     details["deliver_to"] = "data_processing"
        #     details['operation'] = 'task_data'
            # glob_final_data.append(details)
            # proceed_to_deliver(id, details)
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