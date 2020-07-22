#!/usr/bin/env python3
""" Base model """

from datetime import datetime
from typing import TypeVar, List, Dict
import json

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}
DATA['Base'] = {}
DATA['User'] = {}

class Base():
    """ Base class for all models """
    def __init__(self, *args, **kwargs):
        from uuid import uuid4
        classname = self.__class__.__name__
        self.classname = classname
        if not classname in DATA:
            DATA[classname] = {}
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    val = datetime.strptime(val, TIMESTAMP_FORMAT)
                if key != '__class__':
                    if hasattr(val, 'to_json'):
                        setattr(self, key, val.to_json())
                    else:
                        setattr(self, key, val)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        if not hasattr(self, 'id'):
            self.id = str(uuid4())
        self.url = f'https://thepointistochangeit.com/{classname.lower()}s/{self.id}'
        self.image = f'static/images/{classname.lower()}s/{self.id}.'
        DATA[classname][self.id] = self

    @classmethod
    def count(cls) -> int:
        """
        ----------------------------
        Count the number of objects of a given class.
        ----------------------------
        -> Return: Number of objects.
        """
        s_class = cls.__name__
        return len(DATA[s_class].keys())

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """
        ----------------------------
        Search memory for an object of a given class,
        with matching attributes.
        ----------------------------
        -> Return: List of matching objects.
        """
        classname = cls.__name__
        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                try:
                    if (getattr(obj, k) != v):
                        return False
                except Exception:
                    return False
            return True
        return list(filter(_search, DATA[classname].values()))

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """
        ----------------------------
        Get an object by it's id.
        ----------------------------
        -> Return: Object with given id.
        """
        classname = cls.__name__
        return DATA[classname].get(id)

    def __repr__(self):
        """
        ----------------------------
        Generate a string representation of an object.
        ----------------------------
        -> Return: String representation.
        """
        return str(self.__dict__)
    
    def __eq__(self, other: TypeVar('Base')) -> bool:
        """
        ----------------------------
        Test equality of two instances of Base.
        ----------------------------
        -> Return: True or False.
        """
        if type(self) != type(other):
            return False
        if not isintance(other, Base):
            return False
        return self.id == other.id

    def to_json(self) -> dict:
        """
        ----------------------------
        Create a dictionary representation of an object using __dict__.
        ----------------------------
        -> Return: Dictionary representation of object.
        """
        result = {}
        classname = str(self.__class__.__name__)
        result['__classname__'] = classname
        for key, value in self.__dict__.items():
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                if hasattr(value, 'to_json'):
                    result[key] = value.to_json()
                if key == '_id':
                    result[key] = str(value)
                else:
                    if key == 'to_json':
                        continue
                    result[key] = value
        return result

    def save_to_db(self):
        """
        ----------------------------
        Save an object to the database and memory.
        ----------------------------
        -> Return: None.
        """
        from models import db
        db.save_obj(self)

    def update_in_db(self, *args, **kwargs):
        """
        ----------------------------
        Update an object's attributes and then save it
        to the database and memory.
        ----------------------------
        -> Return: None.
        """
        from models import db
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save_to_db()

    def remove_from_db(self):
        """
        ----------------------------
        Remove an object from the database and memory.
        ----------------------------
        -> Return: None.
        """
        from models import db
        db.delete_obj(self)
    
    @classmethod
    def load(cls, db):
        """
        ----------------------------
        Load objects of a given class from the database into memory.
        ----------------------------
        -> Return: None.
        """
        from models import db
        print('loading')
        db.load_class(cls)



if __name__ == "__main__":
    pass