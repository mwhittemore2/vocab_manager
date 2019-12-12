from dict_component import DictionaryComponent

class IndexComponent(DictionaryComponent):
     def create_index(self, params, route):
        conn_method = self.get_connection()
        index_name = params["index_name"]
        seperator = "/"
        index = route + seperator + index_name

        conn_method.send_request(index)
        