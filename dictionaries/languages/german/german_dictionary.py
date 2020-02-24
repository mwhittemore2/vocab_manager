import json

from http import HTTPStatus

from dictionaries.queries import SimpleQuery

class GermanDictionary():
    """
    The German dictionary service.
    """
    def __init__(self, route):
        """
        Initializes the service

        Parameters
        ----------
        route : str
            The path to the Elasticsearch service
        """
        self.set_route(route)

    def format_match(self, match):
        """
        Transforms a dictionary match into its final
        form for user consumption.

        Parameters
        ----------
        match : dict
            A dictionary entry that matched the user's query
        
        Returns
        -------
        dict
            The final form of the dictionary entry
        """
        formatted = []
        if match["inflected_form"] == match["base_form"]:
            for d in match["definitions"]:
                translation = {}
                translation["text"] = match["inflected_form"]
                translation["pos"] = match["pos"]
                translation["definition"] = d
                formatted.append(translation)
        else:
            for d in match["definitions"]:
                translation = {}
                translation["text"] = match["inflected_form"]
                translation["definition"] = d
                
                see_also = {}
                see_also["text"] = match["base_form"]
                see_also["pos"] = match["pos"]
                translation["see_also"] = see_also
                formatted.append(translation)
        
        return formatted
    
    def get_route(self):
        """
        Fetches the route to the Elasticsearch service.

        Returns
        -------
        str
            The route to the Elasticsearch service
        """
        return self.route
    
    def get_top_matches(self, matches, query):
        """
        Ranks exact matches to a user's query at
        the top and then partial matches after.

        Parameters
        ----------
        matches : list
            A list of dictionary entries matching
            the user's query
        query : str
            The words to be translated
        
        Returns
        -------
        list
            A list of translations that have been ranked
            according to the rules above.
        """
        preferred = []
        secondary = []
        query = query.lower()
        for match in matches:
            match = match["_source"]
            if match["inflected_form"].lower() == query:
                m = self.format_match(match)
                preferred += m
            else:
                m = self.format_match(match)
                secondary += m
        
        translations = preferred + secondary
        return translations

    def get_translation(self, query, page, size):
        """
        Finds the dictionary translations of text
        supplied by the user.

        Parameters
        ----------
        query : str
            The text to be translated
        page : int
            The number of the results page
            in the pagination scheme
        size : int
            The number of results per page
        
        Returns
        -------
        json
            The JSON response containing the answers to
            the user's query
        int
            An HTTP status code
        """
        translator = SimpleQuery()
        route = self.get_route()
        params = {}
        params["index_name"] = "german"
        params["page"] = page
        params["size"] = size
        params["term"] = query

        translations = translator.run_query(params, route)
        json_response = json.loads(translations.text)
        
        if "status" in json_response:
            #Presence of 'status' key indicates an error
            response = {}
            response["text"] = "No translations found"
            response = json.dumps(response, ensure_ascii=False)
            return (response, HTTPStatus.NOT_FOUND.value)
        
        translations = json_response["hits"]["hits"]
        if not translations:
            response = {}
            response["text"] = "No translations found"
            response = json.dumps(response, ensure_ascii=False)
            return (response, HTTPStatus.NOT_FOUND.value)

        response = {}
        if page == 1:
            response["translations"] = self.get_top_matches(translations, query)
        else:
            response["translations"] = []
            for t in translations:
                formatted = self.format_match(t["_source"])
                response["translations"] += formatted
        
        response = json.dumps(response, ensure_ascii=False)
        return (response, HTTPStatus.OK.value)
        
    def set_route(self, route):
        """
        Saves the route to the Elasticsearch service.

        Parameters
        ----------
        route : str
            The route to the Elasticsearch service
        """
        self.route = route