from unittest import TestCase

from mongoengine import connect, disconnect
from werkzeug.security import generate_password_hash

from app import create_app
from app.models import User

class BaseTest(TestCase):
    __test__ = False

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.create_user()
        self.username = self.app.config["TEST_USER"]["email"]
        self.password = self.app.config["TEST_USER"]["password"]

    def tearDown(self):
        self.clear_database()
        self.app_context.pop()
    
    def clear_database(self):
        database = self.app.config["MONGODB_SETTINGS"]["db"]
        username = self.app.config["MONGODB_SETTINGS"]["username"]
        password = self.app.config["MONGODB_SETTINGS"]["password"]
        db = connect(db=database, username=username, password=password)
        db.drop_database(database)
        disconnect()
    
    def create_user(self):
        email = self.app.config["TEST_USER"]["email"]
        first_name = self.app.config["TEST_USER"]["first_name"]
        last_name = self.app.config["TEST_USER"]["last_name"]
        password = self.app.config["TEST_USER"]["password"]
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password_hash=generate_password_hash(password)
        )
        user.save()