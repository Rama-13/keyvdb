import os
from flask import Flask, request, jsonify
import json
import threading
from datetime import datetime
from functools import lru_cache
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge, Histogram
# from shared_memory_dict import SharedMemoryDict
# from shared_memory_dict.serializers import JSONSerializer


app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')
lock = threading.Lock()

# db = {SharedMemoryDict(name='tokens', size=1024, serializer=JSONSerializer())}
db = {}
db['data'] = {}
db_size = Gauge('no_of_key', 'Number of Keys')
db_size.set_function(lambda: length())

def search_prefix(key):
    global db
    return dict(filter(lambda item: item[0].startswith(key),db['data'].items()))

def search_suffix(key):
    global db
    return dict(filter(lambda item: item[0].endswith(key),db['data'].items()))

@app.route("/")
def hello_world():
    return "Hello there! Welcome to my In-memory data store!"

@app.route("/len/")
def length():
    global db
    return str(len(db['data']))


@lru_cache(maxsize=32)
@app.route("/get/")
def get_keys():
    global db
    return db


@lru_cache(maxsize=32)
@app.route("/get/<string:id>", methods=["GET"])
def get_key(id):
    global db
    return db['data'].get(id, {})


@app.route("/set/<string:name>", methods=["POST"])
def set_key(name):
    global db
    if name in db['data']:
        return "Key already used"
    lock.acquire()
    db['data'].update({name : request.form.get('value') })
    lock.release()
    return db

@lru_cache(maxsize=32)
@app.route("/search/", methods=["GET"])
def search_key():
    global db
    if 'prefix' in request.args :
        return search_prefix(request.args.get('prefix', ''))
    elif 'suffix' in request.args:
        return search_suffix(request.args.get('suffix', ''))
    return {}

@app.route("/flush/", methods=["GET"])
def flush_db():
    global db
    lock.acquire()
    db['data'] = {}
    lock.release()
    return "DB is flushed"

@app.route("/dumpdb/", methods=["GET"])
def dump_db():
    global db
    lock.acquire()
    currentDT = datetime.now().strftime("%Y%m%d:%H%M%S")
    dir = os.path.join(os.getcwd(), "db-dump", f"{currentDT}.json")
    dir = os.path.join(os.getcwd(), "db-dump", f"{currentDT}.json")
    os.makedirs(os.path.dirname(dir), exist_ok=True)
    with open(f"{dir}", "w+") as f:
        json.dump(db, f, indent=2)
    lock.release()
    return f"Filename: {currentDT}.json"

metrics.register_default(
    metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
),
metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code}),
metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path',
                   labels={'status': lambda r: r.status_code, 'path': lambda: request.path})
)
