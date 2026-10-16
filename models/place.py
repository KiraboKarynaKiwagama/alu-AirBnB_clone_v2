#!/usr/bin/python3
"""Place module"""
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Place class"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place',
                               cascade='all, delete')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False)
    else:
        amenity_ids = []

        @property
        def reviews(self):
            """Reviews of this place (FileStorage)"""
            from models.review import Review
            return [r for r in models.storage.all(Review).values()
                    if r.place_id == self.id]

        @property
        def amenities(self):
            """Amenities of this place (FileStorage)"""
            from models.amenity import Amenity
            return [a for a in models.storage.all(Amenity).values()
                    if a.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Add an Amenity id (only Amenity objects accepted)"""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                if 'amenity_ids' not in self.__dict__:
                    self.amenity_ids = []
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)