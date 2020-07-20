#!/usr/bin/env python3
""" User class """

from models.base import Base



class User(Base):
    """ User class """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User object """
        super().__init__(*args, **kwargs)
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.username = kwargs.get('username')
    def is_valid_password(self, pwd: str) -> bool:
        """
        ----------------------------
        Check if pwd is the same as stored hashed password.
        ----------------------------
        -> Return: True or False
        """
        import bcrypt
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password)
