import argparse
import json

import yaml

from connections import UpdateDictionaryData
from dict_component import DictionaryComponent

class IndexComponent(DictionaryComponent):
    def create_base_form(self, properties, params):
        language = params["language"]
        properties["base_form"] = {}
        base_form = properties["base_form"]
        base_form["type"] = "text"
        base_form["analyzer"] = language

    def create_definitions(self, properties):
        properties["definitions"] = {}
        properties["definitions"]["type"] = "text"

    def create_inflected_form(self, properties, params):
        language = params["language"]
        properties["inflected_form"] = {}
        inflected_form = properties["inflected_form"]
        inflected_form["type"] = "text"
        inflected_form["analyzer"] = language

    def create_pos(self, properties):
        properties["pos"] = {}
        properties["pos"]["type"] = "text"

    def create_word_count(self, properties):
        properties["word_count"] = {}
        properties["word_count"]["type"] = "short"

    def create_properties(self, params):
        self.properties = {}
        
        self.create_base_form(self.properties, params)
        self.create_inflected_form(self.properties, params)
        self.create_definitions(self.properties)
        self.create_pos(self.properties)
        self.create_word_count(self.properties)

    def create_index(self, params):
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