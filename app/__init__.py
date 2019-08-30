from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from config import config

bootstrap = Bootstrap()
db = MongoEngine()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    app.session_interface = MongoEngineSessionInterface(db)

    #setup main routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #add authentication service
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
