import json

from base64 import b64encode

from flask import current_app, g, render_template
from flask_login import login_required

from . import document_viewer

@document_viewer.route("/")
#@login_required
def document_viewer():
    """
    Provides the HTML and associated files for
    viewing documents.
    """

    """user = g.current_user"""

    #Get headers for API calls
    """token_lifetime = current_app.config["AUTH_TOKEN_LIFETIME"]
    auth_token = user.generate_auth_token(expiration=token_lifetime)
    username = user.email
    password = ''
    credentials = b64encode((username + ":" + password).encode('utf-8'))
    credentials = credentials.decode('utf-8')"""
    credentials = "test token"
    headers = {}
    headers["Authorization"] = 'Basic ' + credentials
    headers["Accept"] = 'application/json'
    headers["Content-Type"] = 'application/json'

    #Get microservices
    services = current_app.config["DOCUMENT_VIEWER_SERVICES"]

    #Store user credentials
    logIn = {"headers": headers, "services": services}
    logIn = json.dumps(logIn)

    return render_template('document_viewer/document_manager.html', login=logIn)