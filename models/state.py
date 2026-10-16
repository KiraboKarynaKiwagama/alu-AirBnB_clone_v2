#!/usr/bin/python3
"""State module"""
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State class"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete')
    else:
        @property
        def cities(self):
            """Cities of this state (FileStorage)"""
            from models.city import City
            return [c for c in models.storage.all(City).values()
                    if c.state_id == self.id]