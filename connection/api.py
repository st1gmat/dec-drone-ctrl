import multiprocessing
from flask import Flask, request, jsonify
from uuid import uuid4
import os
from dotenv import load_dotenv
import threading
import base64

load_dotenv()

host_name = "0.0.0.0"
port = os.getenv("CONNECTION_API_PORT", default=5005)

app = Flask(__name__)             # create an app instance

_requests_queue: multiprocessing.Queue = None

@app.route("/connection", methods=['POST'])
def data_ingest():
    content = request.json
    req_id = uuid4().__str__()

    try:
        # base64_content = base64.b64encode(content).decode('utf-8')
        # update_details = {
        #     "id": req_id,
        #     "operation": "data_connection",
        #     "new_data": base64_content,
        #     "deliver_to": "monitor"
        # }
        update_details = {
            "id": req_id,
            "operation": "data_processing",
            "new_data": content,
            "deliver_to": "monitor",
            "deliver_from": "connection"
        }
        _requests_queue.put(update_details)
        print(f"new data event: {update_details}")
    except:
        error_message = f"malformed request {request.data}"
        print(error_message)
        return error_message, 400
    return jsonify({"operation": "new data received", "id": req_id})

def start_rest(requests_queue):
    global _requests_queue 
    _requests_queue = requests_queue
    threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()

if __name__ == "__main__":        # on running python app.py
    start_rest()