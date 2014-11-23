import pytest

from sqlalchemy import event
from sqlalchemy.engine import Engine

import monkeysApp
import monkeysApp.views.main

from monkeysApp.settings import TestConfig
from monkeysApp.app import create_app
from monkeysApp.models import Base


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app("testing", config_obj=TestConfig)
    _app.register_blueprint(monkeysApp.views.main.main_blueprint)

    Base.metadata.create_all(bind=_app.engine)
    _app.connection = _app.engine.connect()
    monkeysApp.app.DbSession.configure(bind=_app.connection)

    yield _app

    _app.connection.close()
    Base.metadata.drop_all(bind=_app.engine)


@pytest.yield_fixture(scope="function")
def session(app):
    """
    Creates a new database session (with working transaction) for a test
    duration.
    """
    app.transaction = app.connection.begin()

    # pushing new Flask application context for multiple-thread tests to work
    ctx = app.app_context()
    ctx.push()

    _session = monkeysApp.app.DbSession()

    yield _session

    # the code after yield statement works as a teardown
    app.transaction.close()
    _session.close()
    ctx.pop()


@pytest.yield_fixture(scope="function")
def test_client(app):
    yield app.test_client()

