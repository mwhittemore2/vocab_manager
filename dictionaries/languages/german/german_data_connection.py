import os

from connections import DataConnection, PostDictionaryData

class GermanDataConnection(DataConnection):
    """
    Connection to the German dictionary service.
    """
    def __init__(self, config):
        """
        Initialize the German dictionary service.

        Parameters
        ----------
        config : str
            A configuration file for the dictionary service
        """
        super().load_params(config)
        conn_method = PostDictionaryData()
        super().set_connection(conn_method)
    
    def write(self, data):
        """
        Writes German dictionary data to Elasticsearch
        needed for the dictionary service.

        Parameters
        ----------
        data : list
            A list of dictionary entries
        """
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