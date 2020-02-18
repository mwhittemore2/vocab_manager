from flask import Blueprint

#Set up API blueprint
api = Blueprint('api', __name__)

from . import authorization, document_retrieval, errors, translation, validation, vocab_acquisition