#!/usr/bin/python3
"""DBStorage module"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """MySQL storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'), getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects (or one class) as {Class.id: obj}"""
        classes = [User, State, City, Amenity, Place, Review]
        if cls is not None:
            if isinstance(cls, str):
                cls = {c.__name__: c for c in classes}.get(cls)
            classes = [cls]
        result = {}
        for c in classes:
            for obj in self.__session.query(c).all():
                result['{}.{}'.format(c.__name__, obj.id)] = obj
        return result

    def new(self, obj):
        """Add obj to session"""
        self.__session.add(obj)

    def save(self):
        """Commit session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and session"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)

    def close(self):
        """Close the session"""
        self.__session.remove()