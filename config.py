#!/usr/bin/python3
import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    USE_DB: bool = os.environ.get('USE_DATABASE', "True").lower() == 'true'
    DB_TYPE: str = os.environ.get('DATABASE_TYPE', 'sqlite')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = Config()
