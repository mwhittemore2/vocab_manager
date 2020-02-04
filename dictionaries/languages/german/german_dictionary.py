import json

from http import HTTPStatus

from dictionaries.queries import SimpleQuery

class GermanDictionary():
    def __init__(self, route):
        self.set_route(route)

    def format_match(self, match):
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
        return self.route
    
    def get_top_matches(self, matches, query):
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
            response["status"] = HTTPStatus.NOT_FOUND.value
            response["text"] = "No translations found"
            response = json.dumps(response, ensure_ascii=False)
            return (response, HTTPStatus.NOT_FOUND.value)
        
        translations = json_response["hits"]["hits"]
        if not translations:
            response = {}
            response["status"] = HTTPStatus.NOT_FOUND.value
            response["text"] = "No translations found"
            response = json.dumps(response, ensure_ascii=False)
            return (response, HTTPStatus.NOT_FOUND.value)

        response = {}
        response["status"] = HTTPStatus.OK.value
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
        self.route = route