from abc import ABC, abstractmethod

import yaml

class DataProcessor(ABC):
    def __init__(self, data_files, config):
        self.store_data(data_files)
        self.load_params(config)
    
    def get_data(self):
        return self.data_files
    
    @abstractmethod
    def get_next_entry(self):
        pass
    
    def load_params(self, config):
        with open(config, 'r') as conf:
            try:
                self.params = yaml.safe_load(conf)
            except Exception as e:
                print("Error loading DataProcessor")
                print(e)
                raise Exception("Couldn't load config file: " + config)

    def store_data(self, data_files):
        self.data_files = data_files