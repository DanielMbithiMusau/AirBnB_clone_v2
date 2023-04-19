#!/usr/bin/env python3
""" This module contains a class BaseModel that
defines all common attributes/methods for other classes.
"""
from datetime import datetime
import uuid
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()

class BaseModel:
    """ Class that defines all common methods/attributes
    for other classes."""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    
    def __init__(self, *args, **kwargs):
        """ Initialization method
        Args:
            args: won't be used.
            kwargs: arguments for the constructor of the BaseModel.

        Attributes:
            id: unique id generated.
            created_at: creation date
            updated_at: updated date
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        value = datetime.strptime(value,
                                                  '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """String represation of class."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    def __repr__(self):
        """Return a string representation."""
        return self.__str__()

    def save(self):
        """ Updates the public instance attribute 'updated_at'
        with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """ Returns a dictionary containing all keys/values
        of __dict__ of the instance. """
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        dict_copy['created_at'] = self.created_at.isoformat()
        dict_copy['updated_at'] = self.updated_at.isoformat()

        if '__sa_instance_state' in dict_copy.keys():
            del dict_copy['__sa_instance_state']
        return dict_copy

    def delete(self):
        """Delete object."""
        models.storage.delete(self)
