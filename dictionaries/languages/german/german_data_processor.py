from itertools import islice

from data_processor import DataProcessor
from languages.german.german_data_handlers import GermanEntryHandler

class GermanDataProcessor(DataProcessor):
    """
    Transforms raw dictionary data into
    Elasticsearch entries.
    """
    def __init__(self, data_files, config):
        """
        Initialize the processor.

        Parameters
        ----------
        data_files = list
            The files to be processed
        config = str
            The path to the configuration file
        """
        super().__init__(data_files, config)
        entry_handler = GermanEntryHandler()
        self.set_handler(entry_handler)

    def get_handler(self):
        """
        Fetches the top-level translation handler

        Returns
        -------
        DataHandler
            The translation handler
        """
        return self.entry_handler

    def get_next_entry(self):
        """
        Fetches the next processed dictionary entry.
        """
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
        """
        Saves the top-level translation handler.

        Parameters
        ----------
        entry_handler : DataHandler
            The top-level translation handler
        """
        self.entry_handler = entry_handler