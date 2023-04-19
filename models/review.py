#!/usr/bin/env python3
"""Module contains class Review that inherits from BaseModel."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class that handles reviews."""
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """Initialization function."""
        super().__init__(*args, **kwargs)
