import os
from pathlib import Path

BASE_DIR = Path().resolve()


class BaseConfig(object):
    DEBUG = os.getenv('DEBUG') in {'1', 'yes', 'true', 'True'}
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{db}'.format(db=BASE_DIR.joinpath('events.sqlite'))


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{db}'.format(db=BASE_DIR.joinpath('dev.sqlite'))


class TestingConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = 'extrasecretstring'  # noqa:S105
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


config = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}
