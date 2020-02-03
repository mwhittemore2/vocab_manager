from unittest import TestCase

from mongoengine import connect, disconnect
from werkzeug.security import generate_password_hash

from app import create_app
from app.models import User

class BaseTest(TestCase):
    """
    This class contains core logic such as setting up a database
    and creating a user which should be run for every test.
    """
    __test__ = False

    def setUp(self):
        """
        Sets up an application context for running a test.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.create_user()
        self.username = self.app.config["TEST_USER"]["email"]
        self.password = self.app.config["TEST_USER"]["password"]

    def tearDown(self):
        """
        Removes any application state after a test completes.
        """
        self.clear_database()
        self.app_context.pop()
    
    def clear_database(self):
        """
        Removes any state in the test database after a test completes.
        """
        database = self.app.config["MONGODB_SETTINGS"]["db"]
        username = self.app.config["MONGODB_SETTINGS"]["username"]
        password = self.app.config["MONGODB_SETTINGS"]["password"]
        db = connect(db=database, username=username, password=password)
        db.drop_database(database)
        disconnect()
    
    def create_user(self):
        """
        Creates a user of the application along with the
        appropriate credentials.
        """
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