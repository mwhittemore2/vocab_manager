import requests

import yaml

from abc import ABC, abstractmethod

class DataConnection(ABC):

    def get_connection(self):
        return self.conn_method

    def load_params(self, config):
        with open(config, 'r') as conf:
            try:
                self.params = yaml.safe_load(conf)
            except Exception as e:
                print("Error loading DataConnection")
                print(e)
                raise Exception("Couldn't load config file: " + config)

    def set_connection(self, conn_method):
        self.conn_method = conn_method

    @abstractmethod
    def write(self, data):
        pass

class DictionaryDataRequest(ABC):
    def __init__(self, timeout=10):
        self.set_timeout(timeout)

    def get_timeout(self):
        return self.timeout

    @abstractmethod
    def request(self, route, data):
        pass

    """def send_request(self, route, params=""):
        try:
            route = "http://" + route
            req = self.request(route, params)

            if not req.status_code >= 200 and req.status_code < 300:
                raise Exception('Received non 200 response')

            #Possibly check if message size is too big here.

            if req.text:
                return req.text
        
        except requests.exceptions.RequestException as e:
            print(e)"""
    
    def set_timeout(self, timeout):
        self.timeout = timeout

class DeleteDictionaryData(DictionaryDataRequest):
    def request(self, route, params=""):
        timeout = self.get_timeout()
        return requests.delete(route, timeout=timeout)

class GetDictionaryData(DictionaryDataRequest):
    def request(self, route, params=""):
        timeout = self.get_timeout()
        if params:
            data = params["data"]
            headers = params["headers"]
            return requests.get(route, data=data, headers=headers, timeout=timeout)    
        return requests.get(route, timeout=timeout)

class PostDictionaryData(DictionaryDataRequest):
    def request(self, route, params=""):
        timeout = self.get_timeout()
        if params:
            data = params["data"]
            headers = params["headers"]
            return requests.post(route, data=data, headers=headers, timeout=timeout)
        return requests.post(route, timeout=timeout)

class UpdateDictionaryData(DictionaryDataRequest):
    def request(self, route, params=""):
        timeout = self.get_timeout()
        if params:
            data = params["data"]
            headers = params["headers"]
            return requests.put(route, data=data, headers=headers, timeout=timeout)
        return requests.put(route, timeout=timeout)