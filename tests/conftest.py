import pytest

from sqlalchemy import event
from sqlalchemy.engine import Engine

import monkeysApp
from monkeysApp.settings import TestConfig
from monkeysApp.app import create_app
from monkeysApp.models import Base


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app("testing", config_obj=TestConfig)

    Base.metadata.create_all(bind=_app.engine)
    _app.connection = _app.engine.connect()
    monkeysApp.app.DbSession.configure(bind=_app.connection)

    yield _app

    _app.connection.close()
    Base.metadata.drop_all(bind=_app.engine)


