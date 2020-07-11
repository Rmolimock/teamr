#!/usr/bin/env python3
""" User class """

import bcrypt
from api.v1.app import db
from models.base import Base



class User(Base):
    """ User class """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User object """
        super().__init__(*args, **kwargs)
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')