import argparse
import json

from connections import UpdateDictionaryData
from dict_component import DictionaryComponent

class TypeComponent(DictionaryComponent):
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

    def create_properties(self, params):
        properties = {}
        
        self.create_base_form(properties, params)
        self.create_inflected_form(properties, params)
        self.create_definitions(properties)
        self.create_pos(properties)

    def create_type(self, params):
        conn_method = self.get_connection()
        index_name = params["index_name"]
        language = params["language"]
        route = params["route"]
        seperator = "/"
        route = route + seperator + index_name 

        data = {}
        data["mappings"] = {"properties":{}}
        properties = data[index_type]["properties"]
        properties = self.create_properties(params)

        data = json.dumps(data)
        response = conn_method.send_request(route, data)
        print(response)

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
    type_comp = TypeComponent(conn_method)
    type_comp.create_type(params)