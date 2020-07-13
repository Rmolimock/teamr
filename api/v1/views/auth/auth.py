
#!/usr/bin/env python3
"""
Authenticate requests and current users.
"""

from flask import request
from uuid import uuid4
from typing import TypeVar
from datetime import datetime


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class Auth():
    """ Authenticate requests and current users. """
    session_ids = {}

    def __init__(self):
        """ empty init for now """
        self.id = str(uuid4())
        self.session_duration = 200

    def save(self):
        from api.v1.app import db
        collection = db['sessions']
        user_id_and_session_exp = Auth.session_ids[self.id]
        session = {self.id: user_id_and_session_exp}
        collection.save(session)

    def create_session(self, user_id):
        """ create a session with expiration """
        if not user_id:
            return None
        if not type(user_id) == str:
            return None
        timestamp = datetime.now()
        Auth.session_ids[self.id] = (user_id, timestamp)
        self.save()
        return self.id

    def user_id_for_session_id(self, session_id=None):
        """ return the user associated with a given session """
        from datetime import datetime, timedelta
        if not session_id:
            return None
        if session_id not in self.session_ids:
            print(2)
            return None
        if not type(self.session_ids[session_id]) == tuple:
            print(3)
            return None
        user_id = Auth.session_ids[session_id][0]
        if self.session_duration <= 0:
            return user_id
        if len(Auth.session_ids[session_id]) != 2:
            print(4)
            return None
        start = Auth.session_ids[session_id][1]
        if datetime.now() > start + timedelta(seconds=self.session_duration):
            print(5)
            return None
        return user_id

    def current_user(self, session_id):
        """ return a user object from given session id """
        from models import User
        user_id = self.user_id_for_session_id(session_id)
        print(user_id, 'user_id')
        if not user_id:
            return None
        user = User.get(user_id)
        if not user:
            return None
        return user_id

    def destroy_session(self, request=None):
        """ logout from current session """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del Auth.session_ids[session_id]
        return True

    def require_auth(self, path, excluded_paths):
        """
        ------------------------------------------------
        Check if requested path requires authentication.
        ------------------------------------------------
        -> Return: True if authentication is required, else False.
        """
        if not path or not excluded_paths or excluded_paths == []:
            return True
        if not isinstance(path, str):
            raise TypeError('path must be a string')
        for excluded in excluded_paths:
            if excluded.endswith("*"):
                excluded = excluded[:-1]
                if path.startswith(excluded):
                    return False
            if path == excluded or path in excluded:
                return False
        return True
    def validate_user(self, e: str, p: str) -> TypeVar('User'):
        """ given a username and password, return the User instance """
        if not e or not isinstance(e, str):
            return None
        if not p or not isinstance(p, str):
            return None
        # ret None if no user with that email
        # same if that user's pwd is wrong
        email = {"email": e}
        from models import User
        user = User.search(email)
        if not user:
            return None
        error = 'incorrect login info'
        return user[0] if user[0].is_valid_password(p) else error
    def session_cookie(self, request):
        return request.cookies.get('activeUser')
