#!/usr/bin/env python3
"""
Route module for the API
"""
# this is the new one
from api.v1.views.auth.auth import Auth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, redirect, render_template
from flask_cors import (CORS, cross_origin)
import os
from models import db
from datetime import datetime, timedelta



# instantiate the app, add cors protection, and check which authentication
# method it should run with.
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})



public_route = ['/api/v1/status/',
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/',
                '/api/v1/views/login/',
                '/auth/login',
                '/auth/login.html',
                '/login',
                '/logout',
                '/register',
                '/reset_password',
                '/reset_password/*',
                '/static/*',
                '/users',
                '/users/*',
                '/teams',
                '/teams/*']

# create the pymongo client and connect to the teamr database


# instantiate the session authentication object
auth = Auth()

def authenticate_current_user(request):
    """
    ----------------------------
    Check if current session is associated with a user.
    ----------------------------
    -> Return: True or abort with approriate errorhandler.
    """
    session = auth.session_exists(request)
    if not session:
        # no session cookie is present
        if auth.require_auth(request.path, public_route):
            # page requested requires authentication
            print('authentication required!')
            abort(401)
        print('good')
        return
    # a session cookie is present
    current_user = auth.current_user(session)
    if not current_user:
        # session cookie is invalid
        if auth.require_auth(request.path, public_route):
            print('authentication required!')
            abort(401)
        print('good t')
        return
    # a session cookie is present and valid
    from models import User
    request.current_user = User.get(current_user)
    print('good to go')



# if route requested needs authentication, authenticate user
@app.before_request
def before():
    """
    ----------------------------
    Check if requested route is public.
    If not, authenticate the user.
    ----------------------------
    -> Return: None or abort with approriate errorhandler.
    """
    from models.user import User
    request.current_user = None
    now = datetime.now()
    delete_expired_sessions()
    if auth:
        authenticate_current_user(request)
        return None


def delete_expired_sessions():
    """
        ----------------------------
        Occasionally delete expired sessions from the db and memory.
        ----------------------------
        -> Return: None.
        """
    for k, v in auth.session_ids.items():
        start = v[1]
        print(k)
        if datetime.now() > start + timedelta(seconds=auth.session_duration):
            del Auth.session_ids[k]

# configure what responses various abort() calls generate
@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def Forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def Unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    # set host and port #s based on environmental variables and run app
    host = getenv("API_HOST", "127.0.0.1")
    port = getenv("API_PORT", "8080")
    app.run(host=host, port=port, debug=True)

