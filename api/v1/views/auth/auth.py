
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
    session_duration = 2000
    def __init__(self):
        """ empty init for now """
        self.id = str(uuid4())
        self.session_duration = 2000
        self.reset_password_tokens = {}
    def create_session(self, user_id):
        """
        ----------------------------
        Create a session for user upon login.
        ----------------------------
        -> Return: newly created session.
        """
        from models import db
        if not user_id:
            return None
        if not type(user_id) == str:
            return None
        timestamp = datetime.now()
        Auth.session_ids[self.id] = [user_id, timestamp]
        db.save_session(self)
        return self.id

    def user_id_for_session_id(self, session_id=None):
        """
        ----------------------------
        Check for a user associated with the current session.
        Verify the session has not expired.
        ----------------------------
        -> Return: User's id or None if error.
        """
        from datetime import datetime, timedelta
        if not session_id:
            return None
        if not session_id in self.session_ids:
            return None
        if not type(self.session_ids[session_id]) == list:
            return None
        user_id = Auth.session_ids[session_id][0]
        if self.session_duration <= 0:
            return user_id
        if len(Auth.session_ids[session_id]) != 2:
            return None
        start = Auth.session_ids[session_id][1]
        if datetime.now() > start + timedelta(seconds=self.session_duration):
            del Auth.session_ids[session_id]
            return None
        return user_id

    def current_user(self, session_id):
        """
        ----------------------------
        Check for a user associated with the current session.
        Verify user exists.
        Update session expiration.
        ----------------------------
        -> Return: User's id or None if error.
        """
        from models import User
        from datetime import datetime
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        print(user_id, 'user_id')
        if not user_id:
            return None
        user = User.get(user_id)
        if not user:
            return None
        Auth.session_ids[session_id][1] = datetime.now()
        return user_id

    def destroy_session(self, request=None):
        """
        ----------------------------
        Destroy the current session to log out user.
        ----------------------------
        -> Return: True or False.
        """
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
        """
        ----------------------------
        Verify a user with given email and password exists.
        ----------------------------
        -> Return: User or error message.
        """
        error = 'Incorrect login credentials.'
        if not e or not isinstance(e, str):
            return error
        if not p or not isinstance(p, str):
            return error
        # ret None if no user with that email
        # same if that user's pwd is wrong
        email = {"email": e}
        from models import User
        user = User.search(email)
        if not user:
            return error
        return user[0] if user[0].is_valid_password(p) else error

    def session_cookie(self, request):
        """
        ----------------------------
        Check for a session cookie.
        ----------------------------
        -> Return: Session cookie or None.
        """
        return request.cookies.get('activeUser')


