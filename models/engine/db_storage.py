#!/usr/bin/python3
"""Module contains class for sqlalchemy."""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """storage engine for database."""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True
                                      )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Class method that returns dictionary."""
        my_dict = {}

        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = f"{type(obj).__name__}.{obj.id}"
                my_dict[key] = obj
        else:
            obj_list = [State, City, User, Place, Review, Amenity]
            for obj_cls in obj_list:
                query = self.__session.query(obj_cls)
                for obj in query:
                    key = f"{type(obj).__name__}.{obj.id}"
                    my_dict[key] = obj
        return my_dict

    def new(self, obj):
        """Adding a new element in table."""
        self.__session.add(obj)

    def save(self):
        """Saving changes that are done."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deleting an object from the table."""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """Configuration of database."""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()


    def close(self):
        """Close all open connections."""
        self.__session.close()
