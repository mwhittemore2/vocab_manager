from flask import Blueprint

#Set up document viewer blueprint
document_viewer = Blueprint('document_viewer', __name__)

from . import views