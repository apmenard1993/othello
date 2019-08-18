import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_config_environment():
    config = 'config.DevelopmentConfig'
    try:
        config = os.environ['APP_SETTINGS']
    except KeyError as k:
        print('Could not determine app settings environment variable. Starting Dev Mode')
    return config


def get_database_url():
    database_url = 'postgresql://localhost:5432/othello'
    try:
        database_url = os.environ['DATABASE_URL']
    except KeyError as k:
        print('Could not determine Database URL environment variable. Defaulting to localhost:5432/othello')
    return database_url


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = get_database_url()


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
