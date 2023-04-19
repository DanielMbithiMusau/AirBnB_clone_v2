#!/usr/bin/env python3
"""Module contains class that serializes instance to a JSON
file and deserializes JSON file to instances.
"""
import json
import os


class FileStorage:
    """Class that serializes instances to a JSON file and
    deserializes JSON file to instances."""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary '__objects'."""
        if cls is not None:
            return {k: v for k, v in FileStorage.__objects.items()
                    if isinstance(v, cls)}
        return FileStorage.__objects

    def new(self, obj):
        """Sets in '__objects' the obj with key."""
        key = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes '__objects' to the JSON file."""
        dict_obj = {}

        for key, value in FileStorage.__objects.items():
            dict_obj[key] = value.to_dict()

        with open(FileStorage.__file_path, 'w', encoding='UTF-8') as f:
            json.dump(dict_obj, f)

    def count(self, cls=None):
        """Count number of objects in storage or count objects
        of a given class."""
        if cls is None:
            return len(FileStorage.__objects)
        else:
            count = 0
            for obj_id in FileStorage.__objects:
                obj = FileStorage.__objects[obj_id]
                if type(obj) == cls:
                    count += 1
            return count

    def reload(self):
        """Deserializes the JSON file to '__objects'."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        dict_obj = {'BaseModel': BaseModel,
                    'User': User,
                    'State': State,
                    'City': City,
                    'Amenity': Amenity,
                    'Place': Place,
                    'Review': Review
                    }

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r', encoding='UTF-8') as f:
                for key, value in json.load(f).items():
                    self.new(dict_obj[value['__class__']](**value))

    def delete(self, obj=None):
        """Deletes an obj from __objects if it's inside. """
        if obj is not None:
            key = f"{type(obj).__name__}.{obj.id}"
            FileStorage.__objects.pop(key, None)
            self.save()
