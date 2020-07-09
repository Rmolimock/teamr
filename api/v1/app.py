#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
import pymongo

# instantiate the app, add cors protection, and check which authentication
# method it should run with.
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["teamr"]
auth = None
auth_type = os.getenv("AUTH_TYPE")
if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()
else:
    pass

'''
@app.before_request
def before():
    """ Check for 401, 403 before request is processed
    """
    if auth:
        # check if the requested route requires authentication
        # an example of a route that does not is /login
        if not auth.require_auth(
                            request.path,
                            ['/api/v1/status/',
                             '/api/v1/unauthorized/',
                             '/api/v1/forbidden/',
                             '/api/v1/auth_session/login/']):
            return
        # verify that either an authorization section exists in
        # the request (for basic authentication) or a session cookie
        # for session authentication
        if not auth.authorization_header(request):
            if not auth.session_cookie(request):
                abort(401)
        # test if this should be inside the if condition too,
        # since it depends on the use of session authentication.
        # verify the session cookie matches that of a current user
        if not auth.current_user(request):
            abort(403)
        # set the request attr 'current_user' to the user
        # corresponding to the provided authentication mechanism
        # - either basicAuth email/pwd or session cookie (session
        # authentication is initially done through login route, which
        # is excluded from authentication)
        request.current_user = auth.current_user(request)
'''

@app.route('/', methods=['GET'], strict_slashes=False)
def landing():
    from flask import render_template
    return render_template('./base.html', user={'hello':'moto'})

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
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
