from flask import jsonify

from . import api

@api.errorhandler(400)
def bad_request(e):
    response = jsonify(status=400, text=str(e))
    return response

@api.errorhandler(401)
def unauthorized(e):
    response = jsonify(status=401, text=str(e))
    return response

@api.errorhandler(403)
def forbidden(e):
    response = jsonify(status=403, text=str(e))
    return response

@api.errorhandler(404)
def resource_not_found(e):
    response = jsonify(status=404, text=str(e))
    return response

@api.errorhandler(500)
def server_error(e):
    response = jsonify(status=500, text=str(e))
    return response