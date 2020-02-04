class DictionaryComponent():
    """
    A component of a foreign language dictionary.
    """
    def __init__(self, conn_method):
        """
        Initializes the component of the dictionary.

        Parameters
        ----------
        conn_method : DictionaryDataRequest
            The mechanism for connecting to a dictionary
        """
        self.set_connection(conn_method)

    def get_connection(self):
        """
        Fetches the mechanism for connecting to a dictionary.

        Returns
        -------
        DictionaryDataRequest
            The mechanism for connecting to a dictionary
        """
        return self.conn_method
    
    def set_connection(self, conn_method):
        """
        Saves the mechanism for connecting to a dictionary.

        Parameters
        ----------
        conn_method : DictionaryDataRequest
            The mechanism for connecting to a dictionary
        """
        self.conn_method = conn_method