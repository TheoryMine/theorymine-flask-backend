import os
import datetime

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
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_LENGTH = datetime.timedelta(days=0, hours=2)
    STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
    STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']



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
    SECRET_KEY = os.getenv('SECRET_KEY') or "\xe4z\xedW\x95\xfa^RX\x87\xc3\xcd$\x9e\xc5\x86\x9a\x0f\x8f\x8a]\xa9*\x8a"
    SESSION_LENGTH = datetime.timedelta(days=1)
    STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
    STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']

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
    SECRET_KEY = os.getenv('SECRET_KEY') or "\xe4z\xedW\x95\xfa^RX\x87\xc3\xcd$\x9e\xc5\x86\x9a\x0f\x8f\x8a]\xa9*\x8a"
    SESSION_LENGTH = datetime.timedelta(days=0, microseconds=500)
    STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
    STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']