#!/usr/bin/python3
"""
thestate class.
"""
from models.base_model import Base, BaseModel
from models.city import City
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os

class State(BaseModel, Base):
    """
    the class for State
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='delete')

    if ("HBNB_TYPE_STORAGE", None) is None:
        @property
        def cities(self):
            Clist = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return Clist
