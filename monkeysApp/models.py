from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from .app import DbSession


class BaseModel(object):
    query = DbSession.query_property()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=BaseModel)


class Monkey(Base):
    """Monkey model"""
    __tablename__ = "monkey"

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True)
    name = Column(String(256))
    age = Column(Integer)

    def __init__(self, email, name, age):
        self.email = email
        self.name = name
        self.age = age


def __repr__(self):
    return self.__str__()


def __str__(self):
    return u'<{} {} {} {}>'.format(self.id, self.email, self.name,
                                  self.age)
