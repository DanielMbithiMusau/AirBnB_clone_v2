#!/usr/bin/env python3
"""Module contains class State that inherits from BaseModel."""
from models.base_model import BaseModel


class State(BaseModel):
    """State class that inherits from BaseModel."""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialization function."""
        super().__init__(*args, **kwargs)
