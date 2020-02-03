from flask import jsonify

from . import api

@api.errorhandler(400)
def bad_request(e):
    response = jsonify(status=400, text=str(e))
    return response

@api.errorhandler(401)
def unauthorized(e):
    """
    Informs the user that he/she is not authorized to access a resource.

    Parameters
    ----------
    e : str
        A custom error message
    
    Returns
    -------
    json
        JSON representation of the error message
    """
    response = jsonify(status=401, text=str(e))
    return response

@api.errorhandler(403)
def forbidden(e):
    """
    Informs the user that he/she is forbidden from accessing a resource.

    Parameters
    ----------
    e : str
        A custom error message
    
    Returns
    -------
    json
        JSON representation of the error message
    """
    response = jsonify(status=403, text=str(e))
    return response

@api.errorhandler(404)
def resource_not_found(e):
    """
    Informs the user that the resource he/she requested wasn't found.

    Parameters
    ----------
    e : str
        A custom error message
    
    Returns
    -------
    json
        JSON representation of the error message
    """
    response = jsonify(status=404, text=str(e))
    return response

@api.errorhandler(500)
def server_error(e):
    """
    Informs the user that there was an error on the server.

    Parameters
    ----------
    e : str
        A custom error message
    
    Returns
    -------
    json
        JSON representation of the error message
    """
    response = jsonify(status=500, text=str(e))
    return response