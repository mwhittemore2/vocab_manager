from flask import Blueprint

#Set up content management blueprint
cm = Blueprint('content_management', __name__)

from . import views