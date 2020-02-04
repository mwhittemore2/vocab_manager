from abc import ABC, abstractmethod

import yaml

class DataProcessor(ABC):
    """
    Base class for reading in data from a data source.
    """
    def __init__(self, data_files, config):
        """
        Initializes the data reader.

        Parameters
        ----------
        data_files : list
            A list of files to read
        config : str
            A path to a configuration file
        """
        self.store_data(data_files)
        self.load_params(config)
    
    def get_data(self):
        """
        Fetches the list of files to read.

        Returns
        -------
        list
            A list of files to read
        """
        return self.data_files
    
    @abstractmethod
    def get_next_entry(self):
        """
        Fetches the next entry to be processed by
        the ETL pipeline.
        """
        pass
    
    def load_params(self, config):
        """
        Saves the parameters necessary for
        reading the data.

        Parameters
        ----------
        config : str
            A path to the configuration file
        """
        with open(config, 'r') as conf:
            try:
                self.params = yaml.safe_load(conf)
            except Exception as e:
                print("Error loading DataProcessor")
                print(e)
                raise Exception("Couldn't load config file: " + config)

    def store_data(self, data_files):
        """
        Saves the names of the files to be read.

        Parameters
        ----------
        data_files : list
            The files to be read
        """
        self.data_files = data_files