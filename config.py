import os

'''
import sys

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
else:
    import urlparse
'''

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:
    APP_NAME = os.environ.get('APP_NAME', 'Soccer')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    '''
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                b'\x003#\x05\x99b`H\x84\xd0 \
                                \x04\x92\x08C\xb5\x9d')

    # token for football data api
    if os.environ.get('AUTH_TOKEN'):
        AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    else:
        AUTH_TOKEN = "AUTH_TOKEN not set"
        print('AUTH_TOKEN not set')

    JSON_DATA_FILENAME = "soccer/assets/2018_matches.json"

    '''
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.sendgrid.net')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', False)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Analytics
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')
    SEGMENT_API_KEY = os.environ.get('SEGMENT_API_KEY', '')

    # Admin account
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')
    ADMIN_EMAIL = os.environ.get(
        'ADMIN_EMAIL', 'flask-base-admin@example.com')
    EMAIL_SUBJECT_PREFIX = '[{}]'.format(APP_NAME)
    EMAIL_SENDER = '{app_name} Admin <{email}>'.format(
        app_name=APP_NAME, email=MAIL_USERNAME)

    REDIS_URL = os.getenv('REDISTOGO_URL', 'http://localhost:6379')

    # Parse the REDIS_URL to set RQ config variables
    if PYTHON_VERSION == 3:
        urllib.parse.uses_netloc.append('redis')
        url = urllib.parse.urlparse(REDIS_URL)
    else:
        urlparse.uses_netloc.append('redis')
        url = urlparse.urlparse(REDIS_URL)

    RQ_DEFAULT_HOST = url.hostname
    RQ_DEFAULT_PORT = url.port
    RQ_DEFAULT_PASSWORD = url.password
    RQ_DEFAULT_DB = 0
    '''

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
                                             'sqlite:///' +
                                             os.path.join(basedir, "soccer",
                                                          'test.db'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    # enables url_for usage
    SERVER_NAME = "localhost.localdomain"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
                                             'sqlite:///' +
                                             os.path.join(basedir, "tests",
                                                          'test123.db'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    DEBUG = False
    USE_RELOADER = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' +
                                             os.path.join(basedir,
                                                          'data.sqlite'))
    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


config = {
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'testing': TestConfig
}
