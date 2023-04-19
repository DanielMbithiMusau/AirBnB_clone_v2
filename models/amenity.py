#!/usr/bin/env python3
"""Module contains class Amenity that inherits from BaseModel."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Class that contains Amenities."""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialization function."""
        super().__init__(*args, **kwargs)
