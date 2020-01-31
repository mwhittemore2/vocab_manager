import yaml

from dictionaries.languages.german.german_dictionary import GermanDictionary

class DictionaryManager():
    def __init__(self, config):
        self.routes_config = config
        self.init_dictionaries()
    
    def get_dictionary(self, language):
        if not self.has_dictionary(language):
            return {}

        return self.dictionaries[language]()

    def get_routes(self):
        routes_config = self.routes_config
        routes = {}
        with open(routes_config, 'r') as conf:
            try:
                routes = yaml.safe_load(conf)
            except Exception as e:
                print("Error loading dictionary routes")
                print(e)
                raise Exception("Couldn't load config file: " + routes_config)
        return routes

    def has_dictionary(self, language):
        return language in self.dictionaries

    def init_dictionaries(self):
        self.dictionaries = {}
        routes = self.get_routes()
        self.dictionaries["german"] = (lambda: GermanDictionary(routes["default"]))
        #Add dictionaries for other languages here