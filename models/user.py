#!/usr/bin/python3
"""
the user class
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

class User(BaseModel, Base):
    """the class for user
    Attributes:
        email: the email address
        password: the password for you login
        first_name: the first name
        last_name: the last name
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    reviews = relationship('Review', backref='user',
                           cascade='delete')
    places = relationship('Place', backref='user',
            cascade='delete')
