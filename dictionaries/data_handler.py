from abc import ABC, abstractmethod

class DataHandler(ABC):
    """
    Base class for transforming a dictionary entry
    to its final form.
    """
    def __init__(self, next_handler):
        """
        Initializes the dictionary entry transformer.

        Parameters
        ----------
        next_handler : DataHandler
            The next transformer to try
        """
        self.set_handler(next_handler)
    
    def get_handler(self):
        """
        Fetches the next transformer if the current one
        is not relevant.

        Returns
        -------
        DataHandler
            The next data transformer
        """
        return self.next_handler

    @abstractmethod
    def process_entry(self, entry):
        """
        Transforms the dictionary entry as specified
        by the derived class.

        Parameters
        ----------
        entry : dict
            An entry for the foreign language dictionary
        """
        pass

    def set_handler(self, next_handler):
        """
        Saves the next transformer to try.

        Parameters
        ----------
        next_handler : DataHandler
            The next data transformer to try
        """
        self.next_handler = next_handler