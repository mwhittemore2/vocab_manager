from flask import current_app, g, jsonify
from flask_httpauth import HTTPBasicAuth

from . import api
from .errors import unauthorized, forbidden
from ..models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(auth_type, password):
    if not auth_type:
        return False

    #Authenticate by token
    if not password:
        g.current_user = User.verify_auth_token(auth_type)
        g.token_used = True
        has_curr_user = g.current_user is not None
        return has_curr_user
    
    #Authenticate by email
    user = User.objects(email=auth_type.lower()).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    is_valid_password = user.verify_password(password)
    return is_valid_password

@auth.error_handler
def auth_error():
    msg = "Credentials are invalid."
    return unauthorized(msg)

@api.before_request
@auth.login_required
def before_request():
    is_unknown = g.current_user.is_anonymous
    is_unconfirmed = g.current_user.confirmed
    if is_unknown and is_unconfirmed:
        msg = "Account is unconfirmed."
        return forbidden(msg)

@api.route('/tokens/', methods=['POST'])
def get_token():
    is_anonymous = g.current_user.is_anonymous
    token_used = g.token_used
    if is_anonymous or token_used:
        msg = "Credentials are invalid."
        return unauthorized(msg)
    
    token_lifetime = current_app.config["AUTH_TOKEN_LIFETIME"]
    auth_token = g.current_user.generate_auth_token(expiration=token_lifetime)
    response = {}
    response["token"] = auth_token
    response["expiration"] = token_lifetime
    response = jsonify(response)
    return response