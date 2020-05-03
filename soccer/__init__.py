import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


def create_app(config="default"):
    app = Flask(__name__)
    app.config.from_object(Config[config])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    Config[config].init_app(app)

    db.init_app(app)
    from . import model
    model.init_app(app)

    '''
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    '''

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
