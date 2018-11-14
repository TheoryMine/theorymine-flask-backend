import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    ENV='production'
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD  =  os.getenv("BASIC_AUTH_PASSWORD")



class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV='development'
    DATABASE_HOST = os.getenv("DATABASE_HOST") or "localhost"
    DATABASE_USER = os.getenv("DATABASE_USER") or "root"
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD") or ""
    DATABASE_NAME = os.getenv("DATABASE_NAME") or "theorymine"
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD  =  os.getenv("BASIC_AUTH_PASSWORD")


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    ENV='test'
    DATABASE_HOST = os.getenv("DATABASE_HOST") or "localhost"
    DATABASE_USER = os.getenv("DATABASE_USER") or "root"
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD") or ""
    DATABASE_NAME = os.getenv("DATABASE_NAME") or "theorymine-test"
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD  =  os.getenv("BASIC_AUTH_PASSWORD")
