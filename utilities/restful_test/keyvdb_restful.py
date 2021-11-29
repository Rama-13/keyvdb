from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
import json
import threading
from datetime import datetime

lock = threading.Lock()

class keyvDB():
    __shared_state = dict()

    def __init__(self):
        self.__dict__=self.__shared_state
        self.db = {}
        self.data = self.db.get("data", {})
    
    def greet(self, name):
        self.set_key(name, "hello!")
        return f"Hello! {name}"

    def search_prefix(self, key):

        return dict(filter(lambda item: item[0].startswith(key),self.data.items()))

    def search_suffix(self, key):
        return dict(filter(lambda item: item[0].endswith(key),self.data.items()))

    def hello_world():
        return "Hello there! Welcome to my In-memory data store!"

    def length(self):
        return str(len(self.data))

    def get_keys(self):
        return json.dumps(self.db)

    def get_key(self, id):
        return self.data.get(id, {})

    def set_key(self, name, value):
        if name in self.data:
            return "Key already used"
        lock.acquire()
        self.data.update({name : value })
        lock.release()
        return self.db

    def search_key(self, prefix=None, suffix=None):
        if 'prefix' :
            return self.search_prefix(prefix)
        elif 'suffix':
            return self.search_suffix(suffix)
        return {}

    def flush_db(self):
        lock.acquire()
        self.data = {}
        lock.release()
        return "DB is flushed"

    def dump_db(self):
        lock.acquire()
        currentDT = datetime.now().strftime("%Y%m%d:%H%M%S")
        dir = os.path.join(os.getcwd(), "db-dump", f"{currentDT}.json")
        os.makedirs(os.path.dirname(dir), exist_ok=True)
        with open(f"{dir}", "w+") as f:
            json.dump(self.data, f, indent=2)
        lock.release()
        return f"Filename: {currentDT}.json"