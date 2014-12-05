__author__ = 'janiniem'
from monkeysApp.models import Monkey


def test_index(test_client):
    with test_client as client:
        rv = client.get('/')
    assert rv.status_code is 200


def test_monkey_add(app, test_client, session):
    data = dict(name="Test Monkey",
                email="test@monkey.com",
                age=12)

    with test_client as client:
        rv = client.post('/monkeys/add', data=data, follow_redirects=True)
        assert rv.status_code is 200
        test_monkey = session.query(Monkey).first()

        assert test_monkey.name == "Test Monkey"
        assert test_monkey.email == "test@monkey.com"
        assert test_monkey.age == 12


def test_monkey_delete(app, test_client, session):
    pass
