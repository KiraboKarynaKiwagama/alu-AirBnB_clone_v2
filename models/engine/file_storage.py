#!/usr/bin/python3
"""FileStorage module"""
import json


class FileStorage:
    """Serializes instances to JSON and back"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return objects, optionally filtered by class"""
        if cls is None:
            return FileStorage.__objects
        name = cls if isinstance(cls, str) else cls.__name__
        return {k: v for k, v in FileStorage.__objects.items()
                if type(v).__name__ == name}

    def new(self, obj):
        """Add obj to __objects"""
        FileStorage.__objects[
            '{}.{}'.format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Save __objects to file"""
        data = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(data, f)

    def delete(self, obj=None):
        """Delete obj from __objects if present"""
        if obj is None:
            return
        key = '{}.{}'.format(type(obj).__name__, obj.id)
        FileStorage.__objects.pop(key, None)

    def reload(self):
        """Load __objects from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
                   'State': State, 'City': City, 'Amenity': Amenity,
                   'Review': Review}
        try:
            with open(FileStorage.__file_path, 'r') as f:
                for key, val in json.load(f).items():
                    FileStorage.__objects[key] = classes[val['__class__']](
                        **val)
        except FileNotFoundError:
            pass