import pytest

from monkeysApp.models import Monkey

@pytest.fixture(scope='function')
def test_monkey(session):
    monkey = Monkey("test_monkey@test.com", "Test Monkey", 12)
    session.add(monkey)
    session.commit()
    return monkey


def test_monkey_relationship(session, test_monkey):
    """
    Make friend requests, assert they exist,
    and accept the friendship
    :param session:
    :param test_monkey:
    :return:
    """
    assert test_monkey.friend_requests_count() == 0
    assert test_monkey.friends.count() == 0

    bob = Monkey("test_friend@test.com", "Friend Monkey", 13)
    friend2 = Monkey("test_friend2@test.com", "Friend Monkey 2", 14)

    # test monkey sends friend request
    test_monkey.friend(bob)
    assert bob.friend_requests_count() == 1

    # bob accepts test_monkey's friend request
    bob.friend(test_monkey)
    assert bob.friend_requests_count() == 0

    # test_monkey and bob sends friend requests to friend2
    test_monkey.friend(friend2)
    bob.friend(friend2)
    assert friend2.friend_requests_count() == 2

    # friend2 denies test_monkey's friend request
    friend2.deny_request(test_monkey)
    # and accepts bob's
    friend2.friend(bob)
    # after all this these should be true
    assert friend2.friend_requests_count() == 0
    assert friend2.is_friend(test_monkey) is False
    assert friend2.is_friend(bob) is True

    session.commit()

