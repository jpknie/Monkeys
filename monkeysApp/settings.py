import os

class Config(object):
	SECRET_KEY = "this is very secret key"
	APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
	PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

class ProductionConfig(Config):
	ENV = 'production'
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'postgresql://janiniem:devpass@localhost/monkeys'

class DevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'postgresql://janiniem:devpass@localhost/monkeys_test'


