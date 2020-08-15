from http import HTTPStatus

from flask import current_app, g, request

from . import api
from .errors import bad_request
from .validation import check_request_params

@api.route('translation/<string:language>', methods=['POST'])
def translation(language):
    """
    Translates a user-specified piece of text.

    Parameters
    ----------
    language : str
        The language to translate from
    
    Returns
    -------
    json
        A JSON representation of the translation
    int
        An HTTP status code
    """
    req_data = request.json

    #Check that the translation query is valid
    params = ["page", "query"]
    msg = check_request_params(req_data, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value
    
    page = int(req_data["page"])
    query = req_data["query"]
    
    #Check that the language to be translated from is supported
    dict_manager = current_app.config["DICTIONARY_MANAGER"]
    if not dict_manager.has_dictionary(language):
        msg = language + " is not a supported language"
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value
    
    #Get the translation
    size = int(current_app.config["TRANSLATIONS_PAGE_SIZE"])
    translator = dict_manager.get_dictionary(language)
    response = translator.get_translation(query, page, size)
    return response[0], response[1]