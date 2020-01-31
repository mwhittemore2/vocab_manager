import os

from dictionaries.dictionary_manager import DictionaryManager

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    AUTH_TOKEN_LIFETIME = os.environ.get('AUTH_TOKEN_LIFETIME') or 3600
    DICTIONARY_ROUTES = os.environ.get('DICTIONARY_ROUTES') or 'dict_routes.yaml'
    DICTIONARY_MANAGER = DictionaryManager(DICTIONARY_ROUTES)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    TRANSLATIONS_PAGE_SIZE = os.environ.get('TRANSLATIONS_PAGE_SIZE') or 25
    VOCAB_ENTRIES_PER_PAGE = os.environ.get('VOCAB_ENTRIES_PER_PAGE') or 50

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'development',
        'username': os.environ.get('MONGODB_DEV_USER'),
        'password': os.environ.get('MONGODB_DEV_PASSWORD')
    }

class TestingConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'testing',
        'username': os.environ.get('MONGODB_TEST_USER'),
        'password': os.environ.get('MONGODB_TEST_PASSWORD')
    }
    TEST_USER = {
        'email': os.environ.get('TEST_USER_EMAIL'),
        'password': os.environ.get('TEST_USER_PASSWORD'),
        'first_name': os.environ.get('TEST_USER_FIRST_NAME'),
        'last_name': os.environ.get('TEST_USER_LAST_NAME')
    }
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig
}