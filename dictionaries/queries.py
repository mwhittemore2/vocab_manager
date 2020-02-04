import json

from abc import ABC, abstractmethod

from dictionaries.connections import GetDictionaryData

class TextQuery(ABC):
    """
    Looks up a user request in a dictionary.
    """
    def __init__(self):
        """
        Initializes the user's translation query.
        """
        conn_method = GetDictionaryData()
        self.set_connection(conn_method)

    @abstractmethod
    def build_query(self, params):
        """
        Builds the query to be sent to the dictionary.

        Parameters
        ----------
        params : dict
            A dictionary of parameters for the query
        """
        pass

    def get_connection(self):
        """
        Fetches the connection to a dictionary service.

        Returns
        -------
        DictionaryDataRequest
            The connection to a dictionary service
        """
        return self.conn_method

    def set_connection(self, conn_method):
        """
        Saves the connection to a dictionary service.

        Parameters
        ----------
        conn_method : DictionaryDataRequest
            The connection to a dictionary service
        """
        self.conn_method = conn_method
    
    def run_query(self, params, route):
        """
        Executes the user's query.

        Parameters
        ----------
        params : dict
            A dictionary of parameters for the query
        route : str
            A path to the dictionary service
        
        Returns
        -------
        json
            The JSON response to the user's query
        """
        seperator = "/"
        search = "_search"
        index_name = params["index_name"]
        route = route + seperator + index_name
        route += seperator + search
        query = self.build_query(params)
        conn_method = self.get_connection()
        lookup = {}
        lookup["data"] = query
        lookup["headers"] = {'Content-Type': 'application/json'}
        return conn_method.request(route, lookup)

class SimpleQuery(TextQuery):
    """
    The most primitive translation query a user can make.
    """
    def build_query(self, params):
        """
        Builds the user's query to be sent to the dictionary
        service.

        Parameters
        ----------
        params : dict
            A dictionary of parameters for the query
        
        Returns
        -------
        json
            A JSON representation of the query
        """
        term = params["term"]
        size = params["size"]
        page = params["page"]

        query = {}
        query["query"] = {"match":{}}
        query["query"]["match"]["inflected_form"] = term

        query["sort"] = []
        query["sort"].append({"_score": "desc"})
        query["sort"].append({"word_count": "asc"})

        query["from"] = (page - 1) * size
        query["size"] = size

        query = json.dumps(query)
        return query

class PhraseQuery(TextQuery):
    """
    A translation query in which a phrase may
    be matched with some fuzziness.
    """
    def build_query(self, params):
        """
        Builds the user's query to be sent to the dictionary
        service.

        Parameters
        ----------
        params : dict
            A dictionary of parameters for the query
        
        Returns
        -------
        json
            A JSON representation of the query
        """
        phrase = params["phrase"]
        slop = params["slop"]

        query = {}
        query["query"] = {"match":{}}

        infl_form = {}
        infl_form["type"] = "phrase"
        infl_form["query"] = phrase
        infl_form["slop"] = slop
        query["query"]["match"]["inflected_form"] = infl_form

        query = json.dumps(query)
        return query