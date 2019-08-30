from mongoengine import *
from . import db

class User(db.Document):
    email = StringField(primary_key=True)
    first_name = StringField()
    last_name = StringField()
    password = StringField()

class Resource(db.EmbeddedDocument):
    name = StringField()
    author = StringField()
    language = StringField()

    meta = {'allow_inheritance': True}

class Book(Resource):
    page_number = IntField()

class Website(Resource):
    url = StringField()
    page_number = IntField()

class VocabWord(db.Document):
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    word = StringField()
    #Mongo uses this field to determine the proper
    #language for the text index
    language = StringField()
    pos = StringField()
    resource = EmbeddedDocumentField(Resource)
    definitions = ListField()

    #Initialize indices
    meta = {'indexes': [
        '$word', 
        'email'
    ]}

class DateRange(db.EmbeddedDocument):
    start_date = DateTimeField()
    end_date = DateTimeField()

class Group(db.Document):
    name = StringField()
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    language = StringField()
    date_ranges = EmbeddedDocumentListField(DateRange)
    pos_types = ListField(StringField())
    authors = ListField(StringField())
    resources = ListField(StringField())

    meta = {'indexes': [
        'email'
    ]}

class TestResult(db.Document):
    name = ReferenceField(Group, reverse_delete_rule=CASCADE)
    email = ReferenceField(Group, reverse_delete_rule=CASCADE)
    test_time = DateTimeField()
    word = StringField()
    is_recognized = BooleanField()

    meta = {'indexes':[
        'name',
        'email'
    ]}

class Page(db.Document):
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    resource = EmbeddedDocumentField(Resource)
    content = StringField()

    meta = {'indexes':[
        'email'
    ]}