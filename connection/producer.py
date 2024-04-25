
import multiprocessing
import threading
from confluent_kafka import Producer
import json

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
        event_details['source'] = 'connection'
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



#     Давайте разберем этот код пошагово:

# 1. **Импорт необходимых модулей:**
#    ```python
#    import multiprocessing
#    import threading
#    from confluent_kafka import Producer
#    import json
#    ```
#    В этом блоке происходит импорт необходимых модулей Python, таких как `multiprocessing`, `threading` и `Producer` из библиотеки `confluent_kafka`, а также модуль `json` для работы с JSON-объектами.

# 2. **Глобальные переменные:**
#    ```python
#    _requests_queue: multiprocessing.Queue = None
#    ```
#    Здесь объявляется глобальная переменная `_requests_queue`, которая представляет собой экземпляр класса `multiprocessing.Queue` и будет использоваться для передачи данных между процессами.

# 3. **Функция `proceed_to_deliver`:**
#    ```python
#    def proceed_to_deliver(id, details):
#        _requests_queue.put(details)
#    ```
#    Это функция, которая помещает переданные ей данные в глобальную очередь `_requests_queue`. Она будет вызываться для обработки доставленных сообщений.

# 4. **Функция `producer_job`:**
#    ```python
#    def producer_job(_, config, requests_queue: multiprocessing.Queue):
#        producer = Producer(config)
#        def delivery_callback(err, msg):
#            if err:
#                print('[error] Message failed delivery: {}'.format(err))
#        topic = "monitor"
#        while True:
#            event_details = requests_queue.get()
#            event_details['source'] = 'connection'
#            producer.produce(topic, json.dumps(event_details), event_details['id'],  
#                callback=delivery_callback
#            )
#            producer.poll(10000)
#            producer.flush()
#    ```
#    Это функция, которая выполняет работу Kafka-производителя. Она получает данные из очереди `_requests_queue`, добавляет к ним дополнительные детали и отправляет их в Kafka-топик "monitor" с помощью экземпляра `Producer`. После отправки сообщения производится опрос брокера Kafka и очистка буфера производителя.

# 5. **Функция `start_producer`:**
#    ```python
#    def start_producer(args, config, requests_queue):
#        global _requests_queue
#        _requests_queue = requests_queue
#        threading.Thread(target=lambda: producer_job(args, config, requests_queue)).start()
#    ```
#    Эта функция запускает процесс работы Kafka-производителя в отдельном потоке. Она устанавливает глобальную переменную `_requests_queue` равной переданной очереди `requests_queue`, а затем запускает функцию `producer_job` в отдельном потоке с использованием модуля `threading`.

# 6. **Блок выполнения приложения:**
#    ```python
#    if __name__ == '__main__':
#        start_producer(None, None, None)
#    ```
#    В этом блоке кода функция `start_producer` вызывается при запуске скрипта. Она передается None в качестве аргументов, потому что мы здесь не используем какие-либо конкретные параметры.