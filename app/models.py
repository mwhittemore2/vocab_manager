from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mongoengine import *
from werkzeug.security import check_password_hash 

from . import db, login_manager 

class User(UserMixin, db.Document):
    email = StringField(primary_key=True)
    first_name = StringField()
    last_name = StringField()
    password_hash = StringField()
    confirmed = BooleanField(default=False)

    def verify_password(self, password):
        self.confirmed = False
        check_hash = check_password_hash(self.password_hash, password)
        if check_hash:
            self.confirmed = True
        return check_hash
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(email=user_id).first()

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"],
                       expires_in=expiration)
        serialized = s.dumps({"email": self.email}).decode("utf-8")
        return serialized
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None

        if "email" not in data:
            return None
            
        user = User.objects(email=data["email"]).first()
        return user

class Resource(db.EmbeddedDocument):
    title = StringField()
    author = StringField()
    language = StringField()
    page_number = IntField()

    meta = {'allow_inheritance': True}

class Book(Resource):
    publisher = StringField()

class Website(Resource):
    url = StringField()

class VocabEntry(db.Document):
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    vocab_text = StringField()
    #Mongo uses this field to determine the proper
    #language for the text index
    language = StringField()
    pos = StringField()
    resource = EmbeddedDocumentField(Resource)
    definitions = ListField()
    timestamp = DateTimeField()

    meta = {'indexes': [
        ('email',
         '$vocab_text', 
         'resource.title',
         'resource.author',
         'resource.page_number')
    ]}

class DateRange(db.EmbeddedDocument):
    start_date = DateTimeField()
    end_date = DateTimeField()

class PageRange(db.EmbeddedDocument):
    start_page = IntField()
    end_page = IntField()

class GroupDefinition(db.EmbeddedDocument):
    title = StringField()
    author = StringField()
    pages = EmbeddedDocumentListField(PageRange)
    dates = EmbeddedDocumentListField(DateRange)

class Group(db.Document):
    group_id = StringField(primary_key=True)
    name = StringField()
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    language = StringField()
    definitions = EmbeddedDocumentListField(GroupDefinition)

    meta = {'indexes': [
        'email'
    ]}

class TestResult(db.Document):
    group_id = ReferenceField(Group, reverse_delete_rule=CASCADE)
    email = StringField()
    test_time = DateTimeField()
    word = StringField()
    is_recognized = BooleanField()

    meta = {'indexes':[
        'group_id',
        'email'
    ]}

class Page(db.Document):
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    resource = EmbeddedDocumentField(Resource)
    content = StringField()

    meta = {'indexes':[
        ('email',
         'resource.page_number',
         'resource.title',
         'resource.author')
    ]}