#!/usr/bin/env python3
""" Auth class """

class Auth():
    pass
    def require_auth(self, path, excluded):
        return None
    def session_cookie(self, request):
        return None
    def current_user(self, request):
        return 'User'