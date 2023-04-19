#!/usr/bin/env python3
""" This module contains a class BaseModel that
defines all common attributes/methods for other classes.
"""
from datetime import datetime
import uuid
from models import storage


class BaseModel:
    """ Class that defines all common methods/attributes
    for other classes."""
    def __init__(self, *args, **kwargs):
        """ Initialization method. """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        value = datetime.strptime(value,
                                                  '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, key, value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """String represation of class."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """ Updates the public instance attribute 'updated_at'
        with the current datetime."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ Returns a dictionary containing all keys/values
        of __dict__ of the instance. """
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        dict_copy['created_at'] = self.created_at.isoformat()
        dict_copy['updated_at'] = self.updated_at.isoformat()

        return dict_copy
