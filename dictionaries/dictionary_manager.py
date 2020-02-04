import yaml

from dictionaries.languages.german.german_dictionary import GermanDictionary

class DictionaryManager():
    """
    Controls access to the different foreign language dictionaries
    that are supported.
    """
    def __init__(self, config):
        """
        Initializes the dictionary manager.

        Parameters
        ----------
        config : str
            A path to the configuration file
        """
        self.routes_config = config
        self.init_dictionaries()
    
    def get_dictionary(self, language):
        """
        Fetches a foreign language dictionary
        query object, if it's supported.

        Parameters
        ----------
        language : str
            The language of the desired dictionary
        
        Returns
        -------
        ForeignLanguageDictionary
            An object for querying a foreign language
            dictionary
        """
        if not self.has_dictionary(language):
            return {}

        return self.dictionaries[language]()

    def get_routes(self):
        """
        Fetches the routes to the foreign language dictionary
        services.
        
        Returns
        -------
        dict
            A dictionary of routes to the dictionary services
        """
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
        """
        Checks if the user-specified language
        has a supporting dictionary

        Parameters
        ----------
        language : str
            The language of the dictionary
        
        Returns
        -------
        bool
            True if the dictionary is supported, False otherwise
        """
        return language in self.dictionaries

    def init_dictionaries(self):
        """
        Loads the foreign language dictionaries.
        """
        self.dictionaries = {}
        routes = self.get_routes()
        self.dictionaries["german"] = (lambda: GermanDictionary(routes["default"]))
        #Add dictionaries for other languages here