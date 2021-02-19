from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mongoengine import *
from werkzeug.security import check_password_hash 

from . import db, login_manager 

class User(UserMixin, db.Document):
    """
    A user of the Vocabulary Manager application.
    """
    email = StringField(primary_key=True)
    first_name = StringField()
    last_name = StringField()
    password_hash = StringField()
    confirmed = BooleanField(default=False)

    def verify_password(self, password):
        """
        Checks that the user-supplied password is correct.

        Parameters
        ----------
        password : str
            The user-supplied password used for authentication
        
        Returns
        -------
        boolean
            True if the user's password is correct, False otherwise.
        """
        check_hash = check_password_hash(self.password_hash, password)
        return check_hash
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Recognizes the user as logged in.

        Parameters
        ----------
        user_id : str
            A unique identifier of the user
        
        Returns
        -------
        User
            An object representation of the user
        """
        return User.objects(email=user_id).first()

    def generate_auth_token(self, expiration):
        """
        Creates an authentication token for access to the
        REST APIs.

        Parameters
        ----------
        expiration : int
            The amount of time in seconds for which the token is valid
        
        Returns
        -------
        token
            The user's authentication token
        """
        s = Serializer(current_app.config["SECRET_KEY"],
                       expires_in=expiration)
        serialized = s.dumps({"email": self.email}).decode("utf-8")
        return serialized
    
    @staticmethod
    def verify_auth_token(token):
        """
        Authenticates the user based on the supplied token.

        Parameters
        ----------
        token : str
            The user-supplied authentication token
        
        Returns
        -------
        User
            An object representation of the authenticated user
        """
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
    """
    An artifact which contains vocabulary words of interest to the user.
    """
    title = StringField()
    author = StringField()
    language = StringField()
    page_number = IntField()

    meta = {'allow_inheritance': True}

class Book(Resource):
    """
    A book the user is reading.
    """
    publisher = StringField()

class Website(Resource):
    """
    A website the user has visited.
    """
    url = StringField()

class VocabEntry(db.Document):
    """
    A vocabulary entry that a user adds to his/her
    vocabulary list.
    """
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
    """
    A span of time of interest to the user.
    """
    start_date = DateTimeField()
    end_date = DateTimeField()

class PageRange(db.EmbeddedDocument):
    """
    A span of pages in a text resource of interest
    to the user.
    """
    start_page = IntField()
    end_page = IntField()

class GroupDefinition(db.EmbeddedDocument):
    """
    A specification for finding specific vocabulary words
    from the user's resource collection.
    """
    title = StringField()
    author = StringField()
    pages = EmbeddedDocumentListField(PageRange)
    dates = EmbeddedDocumentListField(DateRange)

class Group(db.Document):
    """
    A collection of vocabulary words from the user's
    resources.
    """
    group_id = StringField(primary_key=True)
    name = StringField()
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    language = StringField()
    definitions = EmbeddedDocumentListField(GroupDefinition)

    meta = {'indexes': [
        'email'
    ]}

class TestResult(db.Document):
    """
    The results of running a vocabulary retention test.
    """
    group_id = ReferenceField(Group, reverse_delete_rule=CASCADE)
    email = StringField()
    test_time = DateTimeField()
    word = StringField()
    is_recognized = BooleanField()

    meta = {'indexes':[
        'group_id',
        'email'
    ]}

class PageContent(db.EmbeddedDocument):
    """
    The text content of a page from a user's resource.
    """
    words = ListField()
    breaks = DictField()

class Page(db.Document):
    """
    A page in one of the user's resources.
    """
    email = ReferenceField(User, reverse_delete_rule=CASCADE)
    resource = EmbeddedDocumentField(Resource)
    content = EmbeddedDocumentField(PageContent)

    meta = {'indexes':[
        ('email',
         'resource.page_number',
         'resource.title',
         'resource.author')
    ]}
