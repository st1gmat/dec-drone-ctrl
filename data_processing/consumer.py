import threading
from confluent_kafka import Consumer, OFFSET_BEGINNING
import json
from producer import proceed_to_deliver
import os
from dotenv import load_dotenv
# from cryptography.fernet import Fernet
import time

load_dotenv()

# TODO: обсудить где будет храниться drone_id & drone_key
drone_id = os.getenv("DRONE_ID", default=0) # предполгается, что для каждого дрона будет запускаться отдельная группа контейнеров

# def generate_key():
#     return Fernet.generate_key()

# Генерация ключа
# drone_key = b'7IPCWoNeeK4XU1rSToEMoB8voT5ip6r8ww1eRtHRkOI=' # по идеи надо один раз сгенерить его и хранить где-то в env

# Функция для шифрования данных
# def encrypt_data(data, key): # убрать шифрование, оставить комменты
#     cipher_suite = Fernet(key)
#     encrypted_data = cipher_suite.encrypt(json.dumps(data).encode())
#     return encrypted_data

# # Функция для дешифрования данных
# def decrypt_data(encrypted_data, key):
#     cipher_suite = Fernet(key)
#     decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
#     return json.loads(decrypted_data)

# Функция для обработки полученных данных
def processing_received(new_data: bytes, details: dict):
    # Дешифруем данные
    print("Decrypting data....")
    # decrypted_data = decrypt_data(new_data['encrypted-data'], drone_key)
    decrypted_data = new_data
    # print("********")
    if str(drone_id) in decrypted_data["deliver-to"] or decrypted_data["deliver-to"] == "all":
        type = decrypted_data['type']
        if type == "plane_data":
            details["operation"] = "plane_tasks"
        if type == "task_data":
            details["operation"] = "task_data"
    
    return decrypted_data

# Функция для обработки отправленных данных
def processing_departure(new_data: dict, details: dict):
    # Шифруем данные
    print('Encrypting data...')
    new_data["deliver_from"] = str(drone_id)
    # encrypted_data = encrypt_data(new_data, drone_key)
    encrypted_data = new_data
    return encrypted_data

def handle_event(id :str, details: dict):    
    # print(f"[debug] handling event {id}, {details}")
    print(f"[info] handling event {id}, {details['source']}->{details['deliver_to']}: {details['operation']}")
    
    # TODO: сделать остальные компоненты, а то в никуда передается по сути
    try:
        if details['operation'] == 'data_processing':
            new_data = details['new_data']
            if details['source'] == "cooperation_tasks":
                new_data = processing_departure(new_data)
                details['new_data'] = new_data
                details['operation'] = 'data_outputting'
                details['deliver_to'] = 'connection'
                proceed_to_deliver(id, details)

                
            if details['source'] == "connection":
                # new_data = processing_received(new_data, details)
                
                details['new_data'] = new_data
                details['deliver_to'] = 'cooperation_tasks'
                details['operation'] = 'task_data'

                # print('details["deliver_from"] == "connection"\n' + details)
                print("[debug_flag] ended processing_received \n going to deliver")
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
                    print("[debug] consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                        topic=msg.topic(), key=id, value=details_str))
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