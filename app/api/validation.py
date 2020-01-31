def check_request_params(data, params):
    msg = ""
    if type(data) is not dict:
        msg = "JSON request data is in invalid format"
        return msg

    for p in params:
        if p not in data:
            msg = "The following field is required: " + p
            return msg
    return msg 
            