import os

from connections import DataConnection, UpdateDictionaryData

class GermanDataConnection(DataConnection):
    def __init__(self, config):
        super().load_params(config)
        conn_method = UpdateDictionaryData()
        super().set_connection(conn_method)
    
    def write(self, data):
        tmp_file = self.params["tmp_file"]
        route = self.params["route"]
        conn_method = self.get_connection()
        
        with open(tmp_file, encoding="utf-8", mode='w') as tmp:
            output = "".join(data)
            tmp.write(output)
        
        route = route + " @" + tmp_file 
        conn_method.request(route)
        
        os.remove(tmp_file)
        