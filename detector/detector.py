from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from multiprocessing import Queue
from producer import start_producer, proceed_to_deliver
import time
from uuid import uuid4
def detection():
    print("Начало полета и поиска...")
    time.sleep(15)
    print("Обнаружение человека...")

    req_id = uuid4().__str__()
    details = {
        "id": req_id,
        
        "new-data": {
            "status" : "detected",
            "probability": "80%",
            "location": ""
        },
        "deliver_to": "detector_control",
        "operation": "detection"
    }

    proceed_to_deliver(None, details)

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['detector'])

    requests_queue = Queue()
    start_producer(args, config, requests_queue)

    detection()
      