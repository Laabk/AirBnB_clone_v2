#!/usr/bin/python3

from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models.city import City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
import os


class DBStorage:
    """
    activating the databastorage
    """
    __engine = None
    __session = None

    def __init__(self):
        """initialising the object called"""
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')

        try:
            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                    .format(HBNB_MYSQL_USER,HBNB_MYSQL_PWD,HBNB_MYSQL_HOST,
                        HBNB_MYSQL_DB),pool_pre_ping=True)
            if HBNB_ENV is 'test':
                Base.metadata.drop_all(bind=self.__engine)
        except:
            raise
            print("Not Found")

    def all(self, cls=None):
        """calling the list of objectes passed"""
        if cls is None:
            ob = self.__session.query(State).all()
            ob.extend(self.__session.query(User).all())
            ob.extend(self.__session.query(Place).all())
            ob.extend(self.__session.query(Amenity).all())
            ob.extend(self.__session.query(City).all())
            ob.extend(self.__session.query(Review).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            ob = self.__session.query(cls)
        return {"{}.{}".format(type(obj).__name__, obj.id): obj
                for obj in ob}

    def new(self, obj):
        """..creating a object instance"""
        self.__session.add(obj)

    def save(self):
        """..saving the cteated object"""

        self.__session.commit()

    def delete(self, obj=None):
        """this deletes the object"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """this reloads the SQLALchemy session"""
        Base.metadata.create_all(self.__engine)
        s = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(s)
        self.__session = Session()

    def close(self):
        """SQLAlchemy class session class"""
        self.__session.close()
