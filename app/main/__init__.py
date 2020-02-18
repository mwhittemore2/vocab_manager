from flask import Blueprint

#Set up main blueprint
main = Blueprint('main', __name__)

from . import views
