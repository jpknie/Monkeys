import pytest

from monkeysApp.models import Monkey

@pytest.fixture(scope='function')
def test_monkey(session):
    monkey = Monkey("test_monkey@test.com", "Test Monkey", 12)
    session.add(monkey)
    session.commit()
    return monkey

