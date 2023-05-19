#!/usr/bin/env python3
"""Module contains class Amenity that inherits from BaseModel."""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.place import place_amenity

class Amenity(BaseModel, Base):
    """Class that contains Amenities."""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity,
            back_populates="amenities")
