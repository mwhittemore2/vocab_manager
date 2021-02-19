from abc import ABC

class ConfigLoader(ABC):
    """
    Generates a config file from a template.
    """
    def write(params, destination):
        """
        Writes a config file according to the template
        specified by the class that instantiates this
        method.

        Parameters
        ----------
        params : dict
            A dictionary of parameters for the config template.

        destination : str
            The location to write the config file to. 
        """
        pass