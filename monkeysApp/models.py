from sqlalchemy.ext.declarative import declarative_base
from .app import DbSession


class BaseModel(object):
    query = DbSession.query_property()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=BaseModel)
