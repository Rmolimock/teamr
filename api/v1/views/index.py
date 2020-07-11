#!/usr/bin/env python3
"""
Top level API routes
"""
from flask import jsonify, abort, render_template, request
from api.v1.views import app_views
from api.v1.views.auth.auth import Auth
from models import User


auth = Auth()

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    ----------------------------
    Check the status of the API.
    ----------------------------
    -> Return: Json response with status message "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/logout', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
def logout2():
    response = 'LOGGED OUT'
    return render_template('./index.html', debug=response)


@app_views.route('/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
def home():
    """
    -----------------------------
    Check request method and validate user if needed.
    -----------------------------
    -> Return: Public landing page or login redirect page.
    """
    if request.method == "GET":
        if request.cookies.get('debug'):
            return render_template('./index.html', jsonify(request.cookies.get('debug')))
        return render_template('./index.html')
    elif request.method == "POST":
        email, pwd = request.form.get('email'), request.form.get('password')
        # validate_user returns a userJson if True and ErrorMessage if False.
        user_or_error = auth.validate_user(email, pwd)
        if not type(user_or_error) == User:
            return render_template('./index.html', debug=user_or_error)
        return render_template('./index.html', user=user_or_error)


@app_views.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == "GET":
        print("IN HERE")
        return render_template('./auth/register.html')
    if request.method == "POST":
        print("IN HERE YO")
        email, pwd = request.form.get('email'), request.form.get('password')
        user = User()
        user.email = email
        user.password = pwd
        user.save_to_db()
        return render_template('./index.html', debug=(user.id, user.email, user.password))


@app_views.route('/login', methods=['GET'], strict_slashes=False)
def login():
    pass


@app_views.route('/logout', methods=['POST'], strict_slashes=False)
def logout():
    pass
