import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

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

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
