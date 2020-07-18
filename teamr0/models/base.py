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
        print('kwargs:', kwargs)
        classname = self.__class__.__name__
        if not classname in DATA:
            DATA[classname] = {}
        print("OUTSIDE")
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    val = datetime.strptime(val, TIMESTAMP_FORMAT)
                if key != '__class__':
                    setattr(self, key, val)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        if not hasattr(self, 'id'):
            self.id = str(uuid4())
        DATA[classname][self.id] = self

    @classmethod
    def count(cls) -> int:
        """ Count all objects
        """
        s_class = cls.__name__
        return len(DATA[s_class].keys())

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """ Search all objects with matching attributes
        """
        classname = cls.__name__
        print("*", classname)
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
        """ Return one object by ID
        """
        classname = cls.__name__
        return DATA[classname].get(id)

    def __repr__(self):
        return str(self.__dict__)
    
    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Test equality """
        if type(self) != type(other):
            return False
        if not isintance(other, Base):
            return False
        return self.id == other.id

    def to_json(self) -> dict:
            """ Convert the object into a JSON dictionary """
            result = {}
            classname = str(self.__class__.__name__)
            result['__classname__'] = classname
            print('-------------')
            for key, value in self.__dict__.items():
                print(key, value)
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
        """ save instance to the database """
        from models import db
        print('in save ------40988w834089340893890389038903890398039800893209')
        classname = str(self.__class__.__name__)
        print(classname)
        mycol = db[classname]
        dict_repr = self.to_json()
        print('dict of self', dict_repr)
        mycol.save(dict_repr)
        print('saved')

    def remove_from_db(self):
        from models import db
        classname = str(self.__class__.__name__)
        mycol = db[classname]
        dict_repr = self.to_json()
        mycol.delete_one(dict_repr)
    
    @classmethod
    def load(cls, db):
        from models import db
        print('loading')
        classname = cls.__name__
        print(classname)
        mycol = db[classname]
        print(mycol)
        for each in mycol.find():
            print('*')
            obj = cls(**each)


if __name__ == "__main__":
    pass