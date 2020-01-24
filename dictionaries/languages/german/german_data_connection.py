import os

from connections import DataConnection, PostDictionaryData

class GermanDataConnection(DataConnection):
    def __init__(self, config):
        super().load_params(config)
        conn_method = PostDictionaryData()
        super().set_connection(conn_method)
    
    def write(self, data):
        tmp_file = self.params["tmp_file"]
        route = self.params["route"]
        conn_method = self.get_connection()
        
        with open(tmp_file, encoding="utf-8", mode='w') as tmp:
            output = "".join(data)
            tmp.write(output)
        
        data_bin = open(tmp_file, 'rb').read()
        headers = {'Content-Type': 'application/x-ndjson'}
        params = {}
        params["data"] = data_bin
        params["headers"] = headers
        resp = conn_method.request(route, params=params)
        
        os.remove(tmp_file)