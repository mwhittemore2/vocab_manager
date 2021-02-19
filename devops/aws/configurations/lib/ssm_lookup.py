import boto3

class SSMLookup():
    """
    Fetches parameters from the AWS SSM Parameter Store.
    """
    def __init__(self, region):
        """
        Initializes the object that will query the
        parameter store.

        Parameters
        ----------
        region : str
            The AWS region the parameter store is located in.
        """
        self.region = region
    
    def get_params(self, names):
        """
        Fetches the requested parameters
        from the AWS SSM Parameter Store.

        Parameters
        ----------
        names: list
            The parameters to be retrieved.
        
        Returns
        -------
        dict
            The requested parameters.
        """
        #Initialize SSM client
        region = self.get_region()
        ssm = boto3.client('ssm', region)

        #Query the parameter store
        try:
            response = ssm.get_parameters(Names=names)
        except:
            error_msg = "Couldn't connect to parameter store "
            error_msg += "at AWS region " + region
            print(error_msg)

        #Format the results
        params = {}
        for parameter in response["Parameters"]:
            name = parameter["Name"]
            value = parameter["Value"]
            params[name] = value
        
        return params

    def get_region(self):
        """
        Retrieves the AWS region the parameter store
        is located in.

        Returns
        -------
        str
            The AWS region the parameter store is located in.
        """
        return self.region