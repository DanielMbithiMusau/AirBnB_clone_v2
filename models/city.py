#!/usr/bin/env python3
"""Module contains class City that inherits from BaseModel."""
from models.base_model import BaseModel


class City(BaseModel):
    """City class that will generate Cities."""
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialization."""
        super().__init__(*args, **kwargs)
