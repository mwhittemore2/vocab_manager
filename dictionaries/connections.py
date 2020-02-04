import requests

import yaml

from abc import ABC, abstractmethod

class DataConnection(ABC):
    """
    Connection to a data source
    """

    def get_connection(self):
        """
        Fetches the method for connecting to a data source.

        Returns
        -------
        Connection
            The method for connecting to a data source
        """
        return self.conn_method

    def load_params(self, config):
        """
        Saves any parameters required for connecting to
        a data source.

        Parameters
        ----------
        config : str
            The path to the file with the connection parameters
        """
        with open(config, 'r') as conf:
            try:
                self.params = yaml.safe_load(conf)
            except Exception as e:
                print("Error loading DataConnection")
                print(e)
                raise Exception("Couldn't load config file: " + config)

    def set_connection(self, conn_method):
        """
        Saves the method for connecting to a data source.

        Parameters
        ----------
        conn_method : Connection
            The method for connecting to a data source
        """
        self.conn_method = conn_method

    @abstractmethod
    def write(self, data):
        """
        Adds data to a data source.

        Parameters
        ----------
        data : Data
            The data to be written
        """
        pass

class DictionaryDataRequest(ABC):
    """
    Base class for interacting with a
    foreign language dictionary.
    """
    def __init__(self, timeout=60):
        """
        Initializes the request.

        Parameters
        ----------
        timeout : int
            The amount of time to keep the request active
        """
        self.set_timeout(timeout)

    def get_timeout(self):
        """
        Fetches the amount of time to keep the request active.

        Returns
        -------
        int
            The amount of time to keep the request active
        """
        return self.timeout

    @abstractmethod
    def request(self, route, data):
        """
        Sends an HTTP request to a dictionary service.

        Parameters
        ----------
        route : str
            The path to the service
        data : json
            Data to pass to the service
        """
        pass
    
    def set_timeout(self, timeout):
        """
        Saves the amount of time to keep the request active.

        Parameters
        ----------
        timeout : int
            The amount of time to keep the request active
        """
        self.timeout = timeout

class DeleteDictionaryData(DictionaryDataRequest):
    """
    An HTTP DELETE request to a dictionary service.
    """
    def request(self, route, params=""):
        """
        Sends an HTTP DELETE request.

        Parameters
        ----------
        route : str
            The path to the dictionary service
        params : dict
            A dictionary of connection parameters
        
        Returns
        -------
        json
            The JSON response from the DELETE request
        """
        timeout = self.get_timeout()
        return requests.delete(route, timeout=timeout)

class GetDictionaryData(DictionaryDataRequest):
    """
    An HTTP GET request to a dictionary service.
    """
    def request(self, route, params=""):
        """
        Sends an HTTP GET request.

        Parameters
        ----------
        route : str
            The path to the dictionary service
        params : dict
            A dictionary of connection parameters
        
        Returns
        -------
        json
            The JSON response from the GET request
        """
        timeout = self.get_timeout()
        if params:
            data = params["data"]
            headers = params["headers"]
            return requests.get(route, data=data, headers=headers, timeout=timeout)    
        return requests.get(route, timeout=timeout)

class PostDictionaryData(DictionaryDataRequest):
    """
    An HTTP POST request to a dictionary service.
    """
    def request(self, route, params=""):
        """
        Sends an HTTP POST request.

        Parameters
        ----------
        route : str
            The path to the dictionary service
        params : dict
            A dictionary of connection parameters
        
        Returns
        -------
        json
            The JSON response from the POST request
        """
        timeout = self.get_timeout()
        if params:
            data = params["data"]
            headers = params["headers"]
            return requests.post(route, data=data, headers=headers, timeout=timeout)
        return requests.post(route, timeout=timeout)

class UpdateDictionaryData(DictionaryDataRequest):
    """
    An HTTP PUT request to the dictionary service.
    """
    def request(self, route, params=""):
        """
        Sends an HTTP PUT request.

        Parameters
        ----------
        route : str
            The path to the dictionary service
        params : dict
            A dictionary of connection parameters
        
        Returns
        -------
        json
            The JSON response from the PUT request
        """
        timeout = self.get_timeout()
        if params:
            data = params["data"]
            headers = params["headers"]
            return requests.put(route, data=data, headers=headers, timeout=timeout)
        return requests.put(route, timeout=timeout)