#!/usr/bin/env python3
""" Base model """

from datetime import datetime
from typing import TypeVar, List, Dict
import json

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}

class Base():
    """ Base class for all models """
    def __init__(self, *args: list, **kwargs: dict):
        print(kwargs)
        from uuid import uuid4
        classname = '__' + str(self.__class__.__name__) + '__'
        if DATA.get(classname) is None:
            DATA[classname] = {}
        if kwargs:
            self.id = kwargs.get('id', str(uuid.uuid4()))
            if kwargs.get('created_at'):
                self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                    TIMESTAMP_FORMAT)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get('updated_at'):
                self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                    TIMESTAMP_FORMAT)
            else:
                self.updated_at = datetime.utcnow()
            print('each k and v')
            for k, v in kwargs.items():
                setattr(self, k, v)
            self.hello = 42
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            self.email = ''
            self.password = ''
        DATA[classname][self.id] = self

    def __repr__(self):
        return str(self.to_json)
    
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
            classname = '__' + str(self.__class__.__name__) + '__'
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
                        print("IN HERE *&*&*&*&*&*&*&* ")
                        print(k, v)
                        result[key] = str(value)
                    else:
                        result[key] = value
            return result

    def save_to_db(self):
        """ save instance to the database """
        from models import db
        print('in save ------40988w834089340893890389038903890398039800893209')
        classname = '__' + str(self.__class__.__name__) + '__'
        print(classname)
        mycol = db[classname]
        for i in mycol.find():
            print(i)
        dict_repr = self.to_json()
        print('dict of self', dict_repr)
        mycol.save(dict_repr)
        print('saved')

    def remove_from_db(self):
        from models import db
        classname = '__' + str(self.__class__.__name__) + '__'
        mycol = db[classname]
        dict_repr = self.to_json()
        mycol.delete_one(dict_repr)
    
    @classmethod
    def load_from_db(cls):
        from api.v1.app import db
        classname = '__' + str(self.__class__.__name__) + '__'
        mycol = db[classname]
        class_dict = {}
        for each in mycol.find():
            obj = cls(each)
            class_dict[obj.id] = obj
        DATA[obj_dict][classname] = class_dict


if __name__ == "__main__":
    pass