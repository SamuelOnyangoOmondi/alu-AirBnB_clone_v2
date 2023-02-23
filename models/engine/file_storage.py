#!/usr/bin/python3
"""
File Storage Module
"""

import json
import os.path


class FileStorage:
    """
    This class manages serialization and deserialization
    of instances to JSON format to a file
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of every object stored in __objects
        If a class is specified, it returns only the objects of that class
        """
        if cls is None:
            return self.__objects

        return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file
        """
        serialized = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, "w") as file:
            json.dump(serialized, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        """
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r") as file:
                obj_dict = json.load(file)

            for key, value in obj_dict.items():
                class_name, obj_id = key.split(".")
                cls = eval(class_name)
                obj = cls(**value)
                self.__objects[key] = obj

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it exists
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)
