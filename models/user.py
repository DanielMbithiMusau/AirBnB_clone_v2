#!/usr/bin/env python3
"""Module contains class 'User' that inherits
from 'BaseModel'."""
from models.base_model import BaseModel


class User(BaseModel):
    """User class that inherits from BaseModel."""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialization method."""
        super().__init__(*args, **kwargs)
