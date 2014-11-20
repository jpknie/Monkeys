from flask import Flask
from sqlalchemy import create_engine

def create_app(name, config_obj):
	app = Flask(name, template_folder="monkeysApp/templates")
	app.config.from_object(config_obj)

	app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

	return app

