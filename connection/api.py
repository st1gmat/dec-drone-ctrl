import multiprocessing
from flask import Flask, request, jsonify
from uuid import uuid4
import os
from dotenv import load_dotenv
import threading

load_dotenv()

host_name = "0.0.0.0"
port = os.getenv("CONNECTION_API_PORT", default=5005)

app = Flask(__name__)             # create an app instance

_requests_queue: multiprocessing.Queue = None

@app.route("/", methods=['GET'])
def main_connection():
    return "Hello"

def start_rest(requests_queue):
    global _requests_queue 
    _requests_queue = requests_queue
    threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()

if __name__ == "__main__":        # on running python app.py
    start_rest()