#!/usr/bin/python3
"""This creates a file storage class for AirBnB through the
json method"""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models.city import City


class FileStorage:
    """serialization instances to a JSON file and
    deserialization of JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        this will returns a dictionary of the obj
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            class_dict = {}
            for key, val in self.__objects.items():
                if type(val) == cls:
                    class_dict[key] = val
            return class_dict
        return self.__objects

    def new(self, obj):
        """
        transfer the __objects created to given obj
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """
        serializing the file to save JSON file
        """
        ob_path_dict = {obj: self.__objects[obj].to_dict()
                    for obj in self.__objects.keys()}
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(obj_path_dict, f)

    def reload(self):
        """
        serializing the file to JSON
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for obj in json.load(f).values():
                    name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(name)(**obj))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deleting object in the self objects
        """
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """reload method for the objects"""
        self.reload()
