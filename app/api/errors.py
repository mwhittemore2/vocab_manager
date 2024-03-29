from http import HTTPStatus

from flask import jsonify

from . import api

@api.errorhandler(400)
def bad_request(e):
    """
    Informs the user that there is an issue with his/her request.

    Parameters
    ----------
    e : str
        A custom error message

    Returns
    -------
    json
        JSON representation of the error message 
    """
    error_code = HTTPStatus.BAD_REQUEST.value
    response = jsonify(status=error_code, text=str(e))
    return response, error_code

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
    error_code = HTTPStatus.UNAUTHORIZED.value
    response = jsonify(status=error_code, text=str(e))
    return response, error_code

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
    error_code = HTTPStatus.FORBIDDEN.value
    response = jsonify(status=error_code, text=str(e))
    return response, error_code

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
    error_code = HTTPStatus.NOT_FOUND.value
    response = jsonify(status=error_code, text=str(e))
    return response, error_code

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
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    response = jsonify(status=error_code, text=str(e))
    return response, error_code