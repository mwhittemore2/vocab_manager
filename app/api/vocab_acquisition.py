import datetime

from http import HTTPStatus

from flask import current_app, g, jsonify, request
from mongoengine.queryset.visitor import Q

from . import api
from .errors import bad_request, resource_not_found, server_error
from ..models import Resource, VocabEntry
from .validation import check_request_params

def convert_resource(resource_dict, language):
    resource = {}
    title = resource_dict["title"]
    author = resource_dict["author"]
    page_number = resource_dict["page_number"]

    if "type" == "book":
        publisher = "Unknown"
        if "publisher" in resource_dict:
            publisher = resource_dict["publisher"]
        
        resource = Book(title=title,
                        author=author,
                        language=language,
                        page_number=page_number,
                        publisher=publisher
        )
    else:
        resource = Resource(title=resource_dict["title"],
                            author=author,
                            language=language,
                            page_number=page_number
        )
    
    return resource

def get_filter(query, language):
    fil = {}
    if "page" in query:
        has_start = "start" in query["page"]
        has_finish = "finish" in query["page"]
        if has_start and has_finish:
            fil = Q(language=language,
                    resource__title=query["title"],
                    resource__author=query["author"],
                    resource__page_number__gte=query["page"]["start"],
                    resource__page_number__lte=query["page"]["finish"]
                    )
            return fil
            
    fil = Q(language=language,
            resource__title=query["title"],
            resource__author=query["author"]
            )
    return fil

def get_vocab_response(vocab_entry):
    response = {}
    response["vocab_text"] = vocab_entry.vocab_text
    response["title"] = vocab_entry.resource.title
    response["author"] = vocab_entry.resource.author
    response["page"] = vocab_entry.resource.page_number
    #response = jsonify(response)
    return response

@api.route('vocab_acquisition/add_vocab_entry/<string:language>', methods=['POST'])
def add_vocab_entry(language):
    user = g.current_user
    email = user.email
    req_data = request.json

    #Check for vocabulary context
    params = ["vocab_info", "resource"]
    msg = check_request_params(req_data, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value

    vocab_info = req_data["vocab_info"]
    resource = req_data["resource"]
    timestamp = datetime.datetime.now()

    #Check that the resource has a valid structure
    params = ["title", "author", "page_number", "type"]
    msg = check_request_params(resource, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value
    
    #Check vocabulary entry
    params = ["text", "pos", "definitions"]
    msg = check_request_params(vocab_info, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value

    #Insert vocabulary item
    resource = convert_resource(resource, language)
    vocab_entry = VocabEntry(email=email,
                             vocab_text=vocab_info["text"],
                             language=language,
                             pos=vocab_info["pos"],
                             resource=resource,
                             definitions=vocab_info["definitions"],
                             timestamp=timestamp
                             )
    vocab_entry.save()
    check_insert = VocabEntry.objects(email=email,
                                      vocab_text=vocab_info["text"],
                                      language=language,
                                      pos=vocab_info["pos"],
                                      resource=resource,
                                      definitions=vocab_info["definitions"],
                                      timestamp=timestamp
                                      ).first()  
    
    if not check_insert:
        msg = "Couldn't save vocabulary item."
        response = server_error(msg)
        return response

    response = jsonify(status=HTTPStatus.CREATED.value)
    return response, HTTPStatus.CREATED.value

@api.route('vocab_acquisition/lookup_vocab_entry/<string:language>')
def find_vocab_entry(language):
    user = g.current_user
    email = user.email
    req_data = request.json

    #Check for vocabulary information
    params = ["page", "title", "author", "vocab_text"]
    msg = check_request_params(req_data, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value

    page = int(req_data["page"])
    title = req_data["title"]
    author = req_data["author"]
    vocab_text = req_data["vocab_text"]

    #Search for vocabulary entry
    vocab_entry = VocabEntry.objects(vocab_text=vocab_text,
                                     language=language,
                                     resource__title=title,
                                     resource__author=author,
                                     resource__page_number=page
                                     ).first()

    if not vocab_entry:
        msg = "Couldn't find vocabulary entry"
        response = resource_not_found(msg)
        return response, HTTPStatus.NOT_FOUND.value
    
    response = {}
    response["vocab_item"] = get_vocab_response(vocab_entry)
    response["status"] = HTTPStatus.OK.value
    response = jsonify(response)
    return response, HTTPStatus.OK.value

@api.route('vocab_acquisition/lookup_vocab_entries/<string:language>')
def find_vocab_entries(language):
    user = g.current_user
    email = user.email
    req_data = request.json
    
    #Check for presence of user queries
    params = ["page", "queries"]
    msg = check_request_params(req_data, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value

    page = int(req_data["page"])
    entries_per_page = current_app.config["VOCAB_ENTRIES_PER_PAGE"]
    queries = req_data["queries"]

    #Check formatting of user queries
    params = ["title", "author"]
    if type(queries) is not list:
        msg = "No list of queries is given"
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value

    for query in queries:
        msg = check_request_params(query, params)
        if msg:
            response = bad_request(msg)
            return response, HTTPStatus.BAD_REQUEST.value

    #Combine user queries into a single filter
    filters = get_filter(queries[0], language)
    for q in queries[1:]:
        next_filter = get_filter(q, language)
        filters = filters | next_filter
    
    
    #Search for vocabulary entries based on filters
    vocab_entries = VocabEntry.objects(filters)
    vocab_entries = vocab_entries.order_by("vocab_text",
                                           "resource__title",
                                           "resource__author",
                                           "resource__page_number"
                                           )
    paginated = vocab_entries.paginate(page=page,
                                       per_page=entries_per_page
                                       )
    vocab_items = [get_vocab_response(item) for item in paginated.items]

    if not vocab_items:
        msg = "Page contains no vocabulary entries"
        response = resource_not_found(msg)
        return response, HTTPStatus.NOT_FOUND.value

    response = {}
    response["vocab_items"] = vocab_items
    response["page"] = page
    response["status"] = HTTPStatus.OK.value
    response = jsonify(response)
    return response, HTTPStatus.OK.value

@api.route('vocab_acquisition/remove_vocab_entry/<string:language>', methods=['DELETE'])
def remove_vocab_entry(language):
    user = g.current_user
    email = user.email
    req_data = request.json

    #Check for word to remove
    params = ["vocab_text"]
    msg = check_request_params(req_data, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value

    vocab_text = req_data["vocab_text"]

    if "query" in req_data:
        #Check for query parameters
        params = ["title", "author", "page"]
        msg = check_request_params(req_data["query"], params)
        if msg:
            response = bad_request(msg),
            return response, HTTPStatus.BAD_REQUEST.value

        #Delete occurrence of vocab item in a specific text
        query = req_data["query"]
        title = query["title"]
        author = query["author"]
        page_num = int(query["page"])
        to_delete = VocabEntry.objects(vocab_text=vocab_text,
                                       language=language,
                                       resource__title=title,
                                       resource__author=author,
                                       resource__page_number=page_num
                                       )

        if to_delete.first():
            to_delete.delete()
        else:
            msg = "Vocabulary entries to be deleted aren't found"
            response = resource_not_found(msg)
            return response, HTTPStatus.NOT_FOUND.value
    else:
        #Delete all occurrences of vocab item
        to_delete = VocabEntry.objects(vocab_text=vocab_text, language=language)
        if to_delete.first():
            to_delete.delete()
        else:
            msg = "Vocabulary entries to be deleted aren't found"
            response = resource_not_found(msg)
            return response, HTTPStatus.NOT_FOUND.value

    response = jsonify(status=HTTPStatus.NO_CONTENT.value)
    return response, HTTPStatus.NO_CONTENT.value