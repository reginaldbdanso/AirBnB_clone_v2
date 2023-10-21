#!/usr/bin/python3
"""This module is a db_storage engine """
import os

mysql_user = os.environ.get('HBNB_MYSQL_USER')
mysql_pwd = os.environ.get('HBNB_MYSQL_PWD')
mysql_host = os.environ.get('HBNB_MYSQL_HOST')
mysql_db = os.environ.get('HBNB_MYSQL_DB')
mysql_env = os.environ.get('HBNB_ENV')


class DBStorage:
    """This class manages storage of hbnb models in JSON format"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiation of DBStorage class"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker, scoped_session
        from models.base_model import Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                mysql_user,
                mysql_pwd,
                mysql_host,
                mysql_db
                ), pool_pre_ping=True
                )
        if mysql_env == 'test':
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        if cls is None:
            objs = self.__session.query(
                State, City, User, Place, Review, Amenity
                ).all()
        else:
            objs = self.__session.query(classes[cls]).all()
        new_dict = {}
        for obj in objs:
            key = obj.__class__.__name__ + '.' + obj.id
            new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Adds new object to storage dictionary
        (current database session)
        """
        self.__session.add(obj)

    def save(self):
        """
        Saves storage dictionary(commit changes to
        current database session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Loads storage dictionary from database"""
        from models.base_model import BaseModel
        from models.base_model import Base
        from sqlalchemy.orm import sessionmaker, scoped_session
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """Closes the current session"""
        self.__session.remove()
