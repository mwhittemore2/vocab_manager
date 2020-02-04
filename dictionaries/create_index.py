import argparse
import json

import yaml

from connections import UpdateDictionaryData
from dict_component import DictionaryComponent

class IndexComponent(DictionaryComponent):
    """
    The underlying text index for a foreign language dictionary.
    """
    def create_base_form(self, properties, params):
        """
        Initialize the configurations for the
        base form of a dictionary entry.

        Parameters
        ----------
        properties : dict
            A dictionary of index properties
        params : dict
            A dictionary of parameters for
            the base form
        """
        language = params["language"]
        properties["base_form"] = {}
        base_form = properties["base_form"]
        base_form["type"] = "text"
        base_form["analyzer"] = language

    def create_definitions(self, properties):
        """
        Initializes the configurations for the
        definitions of a dictionary entry.

        Parameters
        ----------
        properties : dict
            A dictionary of index properties
        """
        properties["definitions"] = {}
        properties["definitions"]["type"] = "text"

    def create_inflected_form(self, properties, params):
        """
        Initializes the configurations for the inflected
        form of a dictionary entry.

        Parameters
        ----------
        properties : dict
            A dictionary of index properties
        params : dict
            A dictionary of parameters for the
            inflected form
        """
        language = params["language"]
        properties["inflected_form"] = {}
        inflected_form = properties["inflected_form"]
        inflected_form["type"] = "text"
        inflected_form["analyzer"] = language

    def create_pos(self, properties):
        """
        Initializes the configurations for
        a dictionary entry's part of speech.

        Parameters
        ----------
        properties : dict
            A dictionary of index properties
        """
        properties["pos"] = {}
        properties["pos"]["type"] = "text"

    def create_word_count(self, properties):
        """
        Initializes the configuration for the number
        of words in a dictionary entry.

        Parameters
        ----------
        properties : dict
            A dictionary of index properties
        """
        properties["word_count"] = {}
        properties["word_count"]["type"] = "short"

    def create_properties(self, params):
        """
        Initializes the text index's properties.

        Parameters
        ----------
        params : dict
            A dictionary of parameters for the
            various property configurations
        """
        self.properties = {}
        
        self.create_base_form(self.properties, params)
        self.create_inflected_form(self.properties, params)
        self.create_definitions(self.properties)
        self.create_pos(self.properties)
        self.create_word_count(self.properties)

    def create_index(self, params):
        """
        Initializes the text index.

        Parameters
        ----------
        params : dict
            A dictionary of parameters for the
            various property configurations
        """
        conn_method = self.get_connection()
        index_name = params["index_name"]
        route = params["route"]
        seperator = "/"
        route = route + seperator + index_name 

        data = {}
        self.create_properties(params)
        data["mappings"] = {"properties": self.properties}

        params = {}
        params["headers"] = {'Content-Type': 'application/json'}
        data = json.dumps(data)
        params["data"] = data
        response = conn_method.request(route, params)
        print(response.text)

def get_params(config):
    """
    Fetches the parameters necessary for text index creation.

    Parameters
    ----------
    config : str
        A path to the parameters configuration file
    
    Returns
    -------
    dict
        A dictionary containing the parameters for text index
        creation
    """
    params = ""
    with open(config, 'r') as conf:
            try:
                params = yaml.safe_load(conf)
            except Exception as e:
                print("Error creating index")
                print(e)
                raise Exception("Couldn't load config file: " + config)
    
    return params

if __name__ == "__main__":
    #Parse arguments to the script
    parser = argparse.ArgumentParser()
    help_string = "Configuration file for text index creation"
    parser.add_argument("config", help=help_string)
    args = parser.parse_args()

    #Create the text index
    config = args.config
    params = get_params(config)
    conn_method = UpdateDictionaryData()
    index_comp = IndexComponent(conn_method)
    index_comp.create_index(params)