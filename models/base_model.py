#!/usr/bin/python3
"""This is the base model class for AirBnB"""
from uuid import uuid4
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """This class will defines all common attributes/methods
    for other classes
    """
    id = Column(String(60), primary_key=True, nullable=False)
    create_in = Column(DateTime, nullable=False, default=datetime.utcnow())
    update_in = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Instantiation of base model class
        """
        self.id = str(uuid4())
        self.create_in = self.update_in = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """
        returns a string of name, id ...
        """
        dicti = self.__dict__.copy()
        dicti.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, dicti)

    def save(self):
        """
        updates the public instance attribute the to current
        """
        self.update_in = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        creates dictionary of the class
        """
        _dict = self.__dict__.copy()
        _dict["__class__"] = str(type(self).__name__)
        _dict["created_at"] = self.create_in.isoformat()
        _dict["updated_at"] = self.update_in.isoformat()
        _dict.pop("_sa_instance_state", None)
        return _dict

    def delete(self):
        models.storage.delete(self)
