from flask import Blueprint

#Set up authentication blueprint
auth = Blueprint('auth', __name__)

from . import views