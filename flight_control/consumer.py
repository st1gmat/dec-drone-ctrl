import threading
from confluent_kafka import Consumer, OFFSET_BEGINNING
import json
from producer import proceed_to_deliver


def handle_event(id, details):    
    # print(f"[debug] handling event {id}, {details}")
    print(f"[info] handling event {id}, {details['source']}->{details['deliver_to']}: {details['operation']}")
    try:
        if details["source"] == "technical_data":
            print("Recieving and analyzing techical_data")
            print("If something is wrong this component calls emergency_landing")
            
            # Закомментированное - это негативный сценарий (который не реализуем)
            # details["deliver-to"] = "emergency_landing"
            # details['operation'] = 'alert'
            # proceed_to_deliver(id, details)
        
        if details["source"] == "navigation":
            print("Recieving and analyzing navigation data")
            print("If something is wrong this component calls emergency_landing")
            # Закомментированное - это негативный сценарий (который не реализуем)
            # details["deliver-to"] = "emergency_landing"
            # details['operation'] = 'alert'

            details["deliver-to"] = "cooperation_plane"
            details['operation'] = 'movement_data'

            proceed_to_deliver(id, details)

        if details["source"] == "cooperation_plane":
            print("Processing of plane_data & task_data -> to movement_data, which sends them to motor_control")
            details["deliver-to"] = "motor_control"
            details['operation'] = 'movement_data'
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