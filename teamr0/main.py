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

# instantiate the app, add cors protection, and check which authentication
# method it should run with.
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# create the pymongo client and connect to the teamr database


# instantiate the session authentication object
auth = Auth()

# if route requested needs authentication, authenticate user
@app.before_request
def before():
    """ Check for 401, 403 before request is processed
    """
    if auth:

        if not auth.require_auth(
                            request.path,
                            ['/api/v1/status/',
                             '/api/v1/unauthorized/',
                             '/api/v1/forbidden/',
                             '/api/v1/views/login/',
                             '/auth/login',
                             '/auth/login.html',
                             '/login',
                             '/logout',
                             '/register',
                             '/api/v1/views/register',
                             '/static/*']):
            return None
        session = auth.session_cookie(request)
        if not session:
            abort(401)
        current_user = auth.current_user(session)
        if not current_user:
            abort(403)


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