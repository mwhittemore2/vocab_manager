from http import HTTPStatus

from flask import g, jsonify, request

from . import api
from .errors import bad_request, resource_not_found
from ..models import Page
from .validation import check_request_params

@api.route('/document_retrieval/fetch_page')
def fetch_page():
    user = g.current_user
    email = user.email
    req_data = request.json

    #Check for document information
    params = ["title", "author", "page"]
    msg = check_request_params(req_data, params)
    if msg:
        response = bad_request(msg)
        return response, HTTPStatus.BAD_REQUEST.value
    
    title = req_data["title"]
    author = req_data["author"]
    page_num = int(req_data["page"])

    #Search for the requested page
    page = Page.objects(email=email,
                        resource__title=title,
                        resource__author=author,
                        resource__page_number=page_num
                        ).first()
    
    if not page:
        msg = "Couldn't retrieve requested page"
        response = resource_not_found(msg)
        return response, HTTPStatus.NOT_FOUND.value

    response = {}
    response["status"] = HTTPStatus.OK.value
    response["title"] = title
    response["author"] = author
    response["page"] = page_num
    response["content"] = page.content
    
    response = jsonify(response)
    return response, HTTPStatus.OK.value

@api.route('/document_retrieval/list_docs')
def list_docs():
    user = g.current_user
    email = user.email

    #Find all the user's documents
    docs = Page.objects(email=email, resource__page_number=1)
    docs = docs.order_by('resource__title','resource__author')
    
    if not docs:
        msg = "Couldn't find user's documents"
        response = resource_not_found(msg)
        return response, HTTPStatus.NOT_FOUND.value
    
    #Collect document names into a response
    works = []
    for doc in docs:
        work = {"title": doc.resource.title,
                "author": doc.resource.author}
        works.append(work)
    
    response = jsonify({"docs": works, "status": HTTPStatus.OK.value})
    return response, HTTPStatus.OK.value