def check_request_params(data, params):
    """
    Checks that a JSON request contains the proper parameters.

    Parameters
    ----------
    data : json
        The JSON request
    params: list
        The parameters that should appear in the JSON request
    
    Returns
    -------
    str
        A message detailing validation errors, if any
    """
    msg = ""
    if type(data) is not dict:
        msg = "JSON request data is in invalid format"
        return msg

    for p in params:
        if p not in data:
            msg = "The following field is required: " + p
            return msg
    return msg     