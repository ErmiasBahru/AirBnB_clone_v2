#!/usr/bin/python3
""" Module defines the class DBStorage that manages db storage for
    hbnb clone
"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base, BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """This class manages storage of hbnb models in db system"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ queries on the current database session (self.__session) all
            objects depending of the class name (argument cls)
        """
        objs_list = []
        if cls is None:
            all_cls = [City, Place, Review, State, User, Amenity]
            for obj in all_cls:
                objs_list.extend(self.__session.query(obj).all())
        else:
            if type(cls) == str:
                cls = classes[cls]
            elif cls not in classes.values():
                return
            objs_list = self.__session.query(cls).all()

        objs_dict = {"{}.{}".format(v.__class__.__name__,
                                    v.id): v for v in objs_list}
        return objs_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and initialize a
            new session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
            This clears all items and ends any transaction in progress
        """
        self.__session.close()
