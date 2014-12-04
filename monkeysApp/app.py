from __future__ import absolute_import

from flask import Flask, _app_ctx_stack, abort
from flask.ext.login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Query as SAQuery
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


DbSession = scoped_session(sessionmaker(),
                           # __ident_func__ should be hashable, therefore used
                           # for recognizing different incoming requests
                           scopefunc=_app_ctx_stack.__ident_func__)

login_manager = LoginManager()


class BaseQuery(SAQuery):
    """
    Extended SQLAlchemy Query class, provides :meth:`BaseQuery.first_or_404`
    and :meth:`BaseQuery.get_or_404` similarily to Flask-SQLAlchemy.
    These methods are additional, :class:`BaseQuery` works like a normal
    SQLAlchemy query class.
    """

    def get_or_404(self, identity):
        result = self.get(identity)
        if result is None:
            abort(404)
        return result

    def first_or_404(self):
        result = self.first()
        if result is None:
            abort(404)
        return result


def create_app(name, config_obj):
    app = Flask(name, template_folder="monkeysApp/templates")
    app.config.from_object(config_obj)

    app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    global DbSession
    DbSession.configure(bind=app.engine, query_cls=BaseQuery)

    @app.teardown_appcontext
    def teardown(exception=None):
        if isinstance(exception, NoResultFound) or \
                isinstance(exception, MultipleResultsFound):
            abort(404)
        global DbSession
        if DbSession:
            DbSession.remove()

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    global login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'login'


import monkeysApp.views.main


def register_blueprints(app):
    app.register_blueprint(monkeysApp.views.main.main_blueprint)
    return None
