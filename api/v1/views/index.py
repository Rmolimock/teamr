#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, render_template, url_for, request
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/logout/', methods=['GET'], strict_slashes=False)
def logout():
    return render_template('./auth/logout.html')


@app_views.route('/login/', methods=['POST'], strict_slashes=False)
def login_():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template('./auth/login.html', error="bad format")
    return render_template('./base.html')


@app_views.route('/login/', methods=['GET'], strict_slashes=False)
def login():
    return render_template('./auth/login.html')


@app_views.route('/register/', methods=['GET', 'POST'], strict_slashes=False)
def register():
    from models.base import Base
    from flask import redirect
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template('./auth/register.html', error="bad format")
    u = {'email': email, 'password': password}
    user = Base(u)
    fuser = user.to_json()
    return redirect('/')