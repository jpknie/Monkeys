from __future__ import absolute_import

from flask import Flask, _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Query as SAQuery


DbSession = scoped_session(sessionmaker(),
                           # __ident_func__ should be hashable, therefore used
                           # for recognizing different incoming requests
                           scopefunc=_app_ctx_stack.__ident_func__)


def create_app(name, config_obj):
    app = Flask(name, template_folder="monkeysApp/templates")
    app.config.from_object(config_obj)

    app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    return app

