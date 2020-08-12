import os

from dictionaries.dictionary_manager import DictionaryManager
from text_processing.tokenizers.mapper import TokenizerMapper

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    AUTH_TOKEN_LIFETIME = os.environ.get('AUTH_TOKEN_LIFETIME') or 3600
    DICTIONARY_ROUTES = os.environ.get('DICTIONARY_ROUTES') or 'dict_routes.yaml'
    DICTIONARY_MANAGER = DictionaryManager(DICTIONARY_ROUTES)
    DOCUMENT_UPLOAD = {}
    DOCUMENT_UPLOAD["BATCH_SIZE"] = os.environ.get("DOCUMENT_UPLOAD_BATCH_SIZE") or 100
    DOCUMENT_UPLOAD["EARLY_CUTOFF"] = os.environ.get("DOCUMENT_UPLOAD_EARLY_CUTOFF") or 0
    DOCUMENT_UPLOAD["LINE_SIZE"] = os.environ.get("DOCUMENT_UPLOAD_LINE_SIZE") or 50
    DOCUMENT_UPLOAD["PAGE_LIMIT"] = os.environ.get("DOCUMENT_UPLOAD_PAGE_LIMIT") or 30
    DOCUMENT_VIEWER_SERVICES = {
        "getPages": "http://localhost:1080/page_range",
        "getTranslations": "http://localhost:1080/translations",
        "listDocuments": "http://localhost:1080/document_retrieval/doc_list"
    }
    LANGUAGE_OPTIONS = [('english', 'English'), ('german', 'German')]
    PAGE_RANGE_DEFAULT_SIZE = os.environ.get("PAGE_RANGE_DEFAULT_SIZE") or 5
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    TOKENIZER = TokenizerMapper()
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
    TEST_DOCUMENT_UPLOAD = {
        'doc_location': os.environ.get('TEST_DOC_UPLOAD_DOC_LOCATION'),
        'doc_metadata': os.environ.get('TEST_DOC_UPLOAD_DOC_METADATA'),
        'page_limit': os.environ.get('TEST_DOC_UPLOAD_PAGE_LIMIT'),
        'line_size': os.environ.get('TEST_DOC_UPLOAD_LINE_SIZE'),
        'batch_size': os.environ.get('TEST_DOC_UPLOAD_BATCH_SIZE')
    }
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig
}