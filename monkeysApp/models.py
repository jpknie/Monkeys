from sqlalchemy import Integer, String, Column, ForeignKey, select
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from monkeysApp.app import DbSession as db


class BaseModel(object):
    query = db.query_property()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=BaseModel)

friendships = Table('friendships',
                    Base.metadata,
                    Column('user_id', Integer, ForeignKey('monkey.id')),
                    Column('friend_id', Integer, ForeignKey('monkey.id'))
)

monkey_friend_requests = Table('friend_requests',
                               Base.metadata,
                               Column('user_id', Integer, ForeignKey('monkey.id')),
                               Column('requester_id', Integer, ForeignKey('monkey.id'))
)


class Monkey(Base):
    """Monkey model"""
    __tablename__ = "monkey"

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True)
    name = Column(String(256))
    age = Column(Integer)
    password = Column(String(256))
    friends = relationship('Monkey',
                           secondary=friendships,
                           primaryjoin=(friendships.c.user_id == id),
                           secondaryjoin=(friendships.c.friend_id == id),
                           backref=backref('friendships', lazy='dynamic'),
                           lazy='dynamic')

    friend_requests = relationship('Monkey',
                                   secondary=monkey_friend_requests,
                                   primaryjoin=(monkey_friend_requests.c.user_id == id),
                                   secondaryjoin=(monkey_friend_requests.c.requester_id == id),
                                   backref=backref('monkey_friend_requests', lazy='dynamic'),
                                   lazy='dynamic')


    def __init__(self, email='', name='', age='', password=''):
        self.email = email
        self.name = name
        self.age = age
        self.password = password

    def request(self, other_monkey):
        if (not other_monkey in self.friend_requests) and (not self in other_monkey.friend_requests):
            self.friend_requests.append(other_monkey)

    def friend_requests_count(self):
        return self.friend_requests.count()

    def friend(self, monkey):
        """
            Make a friend monkey
            :param monkey to be friended
        """
        if monkey.id != self.id:
            # Check if they are already friends
            if not self.is_friend(monkey):
                # Check if the other user has sent friend request
                if monkey in self.friend_requests:
                    # Accept the friendship
                    self.friends.append(monkey)
                    # Remove the old friend request
                    self.friend_requests.remove(monkey)
                    # Initiate friend request
                else:
                    monkey.request(self)

    def deny_request(self, monkey):
        """
            Deny the friend request
            :param monkey: monkey to deny request from
            :return:
        """
        if monkey in self.friend_requests:
            self.friend_requests.remove(monkey)

    def is_friend(self, monkey):
        """
            Check if monkey is the friend of this
            :param monkey: the monkey to check against
            :return: True if friends
        """
        if (monkey in self.friends) or (self in monkey.friends):
            return True
        return False

    def remove_friend(self, monkey):
        if monkey in self.friends:
            self.friends.remove(monkey)
        if self in monkey.friends:
            monkey.friends.remove(self)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return u'<{} {} {} {}>'.format(self.id, self.email, self.name,
                                       self.age)


friendship_union = select([
    friendships.c.friend_id,
    friendships.c.user_id
]).union(
    select([
        friendships.c.user_id,
        friendships.c.friend_id]
    )
).alias()

Monkey.all_friends = relationship('Monkey',
                                  secondary=friendship_union,
                                  primaryjoin=(Monkey.id == friendship_union.c.friend_id),
                                  secondaryjoin=(Monkey.id == friendship_union.c.user_id),
                                  viewonly=True)
