from itertools import islice

from data_processor import DataProcessor
from languages.german.german_data_handlers import GermanEntryHandler

class GermanDataProcessor(DataProcessor):
    def __init__(self, data_files, config):
        super().__init__(data_files, config)
        entry_handler = GermanEntryHandler()
        self.set_handler(entry_handler)

    def get_handler(self):
        return self.entry_handler

    def get_next_entry(self):
        data_files = self.get_data()
        entry_handler = self.get_handler()
        threshold = self.params["data_threshold"]["read"]

        for data_file in data_files:
            with open(data_file, encoding='utf-8', mode='r') as data:
                empty_cache = False
                while(not empty_cache):
                    cache = list(islice(data, threshold))
                    if not cache:
                        empty_cache = True
                        continue
                    
                    for line in cache:
                        entries = entry_handler.process_entry(line)
                        yield entries
    
    def set_handler(self, entry_handler):
        self.entry_handler = entry_handler