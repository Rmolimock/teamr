
#!/usr/bin/env python3
"""
Authenticate requests and current users.
"""

from flask import request


class Auth():
    """ Authenticate requests and current users. """
    def __init__(self):
        pass

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
    def validate_user(self, email, pwd):
        from api.v1.app import db
        collection = db['User']
        credentials = {'email': email, 'password': pwd}
        document = collection.find_one(credentials)
        if document:
            return document
        return {'error': 'incorrect username or password'}
    def session_cookie(self, request):
        return None
    def current_user(self, request):
        return None