import yaml

class DataWriter():
    def __init__(self, data_conn, data_proc, config):
        self.data_conn = data_conn
        self.data_proc = data_proc
        self.load_params(config)
    
    def load_params(self, config):
        with open(config, 'r') as conf:
            try:
                self.params = yaml.safe_load(conf)
            except Exception as e:
                print("Error loading DataWriter")
                print(e)
                raise Exception("Couldn't load config file: " + config)
    
    def write(self, data_files):
        data_proc = self.data_proc(data_files)
        data_conn = self.data_conn
        threshold = self.params["data_threshold"]["write"]
        data_stream = []
        for entry in data_proc.get_next_entry():
            data_stream += entry
            if len(data_stream) >= threshold:
                data_conn.write(data_stream)
                data_stream = []
        
        if data_stream:
            data_conn.write(data_stream)