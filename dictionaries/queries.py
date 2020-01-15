import json

from abc import ABC, abstractmethod

from connections import GetDictionaryData

class TextQuery(ABC):
    def __init__(self):
        conn_method = GetDictionaryData()
        self.set_connection(conn_method)

    @abstractmethod
    def build_query(self, params):
        pass

    def get_connection(self):
        return self.conn_method

    def set_connection(self, conn_method):
        self.conn_method = conn_method
    
    def run_query(self, params, route):
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
    def build_query(self, params):
        term = params["term"]
        
        query = {}
        query["query"] = {"match":{}}
        query["query"]["match"]["inflected_form"] = term

        query["sort"] = []
        query["sort"].append({"_score": "desc"})
        query["sort"].append({"word_count": "asc"})

        query = json.dumps(query)
        return query

class PhraseQuery(TextQuery):
    def build_query(self, params):
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