__author__ = 'janiniem'


def test_index(test_client):
    with test_client as client:
        rv = client.get('/')
    assert "Hello world!" in rv.data

