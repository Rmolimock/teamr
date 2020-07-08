#!/usr/bin/env python3
"""
Route module for the API
"""
from auth import Auth
from os import getenv
from flask import Flask, jsonify, abort, request, render_template
from flask_cors import (CORS, cross_origin)
import os
from views import app_views


# instantiate the app and add cors protection
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "*"}})
auth = Auth()


@app.before_request
def before():
    """ Check for 401, 403 before request is processed
    """
    if auth:
        if not auth.require_auth(
                            request.path,
                            ['/status/',
                             '/unauthorized/',
                             '/forbidden/',
                             '/login/',
                             '/landing/']):
            return None
        if not auth.session_cookie(request):
            abort(401)
        user = auth.current_user(request)
        if not user:
            abort(403)
        request.current_user = auth.current_user(request)


@app.route('/', methods=['GET'], strict_slashes=False)
def landing():
    return render_template('./base.html')


@app.route('/logout/', methods=['GET'], strict_slashes=False)
def logout():
    return render_template('./auth/logout.html')


@app.route('/login/', methods=['POST'], strict_slashes=False)
def login_():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template('./auth/login.html', error="bad format")
    return jsonify({email: password})


@app.route('/login/', methods=['GET'], strict_slashes=False)
def login():
    return render_template('./auth/login.html')


@app.route('/register/', methods=['GET', 'POST'], strict_slashes=False)
def register():
    return render_template('./auth/register.html')


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
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
