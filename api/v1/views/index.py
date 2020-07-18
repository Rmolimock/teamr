#!/usr/bin/env python3
"""
Top level API routes
"""
from flask import jsonify, abort, render_template, request, redirect, make_response
from api.v1.views import app_views
from api.v1.views.auth.auth import Auth
from models import User


auth = Auth()

@app_views.route('/me', methods=['GET'], strict_slashes=False)
def user_page():
    session = auth.session_cookie(request)
    user_id = auth.current_user(session)
    user = User.get(user_id)
    if not user:
        return redirect('./auth/login.html')
    user_dict = user.to_json()
    return render_template('./profile.html', user=user_dict)
    

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


@app_views.route('/', methods=['GET'], strict_slashes=False)
def home():
    """
    -----------------------------
    Check if logged in and render landing page.
    -----------------------------
    -> Return: Public landing page.
    """
    session_id = request.cookies.get('activeUser')
    users = User.search()
    return render_template('./index.html', all_users=users, session_id=session_id)
        
        


@app_views.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    -----------------------------
    Check request method and register user if acceptable credentials.
    -----------------------------
    -> Return: Profile page if successful, otherwise /register with error.
    """
    from models import db
    if request.method == "GET":
        return render_template('./auth/register.html')
    if request.method == "POST":
        uname = request.form.get('username')
        email = request.form.get('email')
        pwd = request.form.get('password')
        user = db.register(uname, email, pwd)
        if not type(user) == User:
            return render_template('./auth/register.html', debug=user)
        session_id = auth.create_session(user.id)
        response = make_response(render_template('./profile.html', user=user))
        response.set_cookie('activeUser', session_id)
        return response


@app_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template('./auth/login.html')
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        if not '@' in email:
            return render_template('./auth/login.html', debug='Incorrect login credentials.')
        user_or_error = auth.validate_user(email, pwd)
        users = User.search()
        if not type(user_or_error) == User:
            return render_template('./index.html', debug=user_or_error, all_users=users)
        user = user_or_error
        session_id = auth.create_session(user.id)
        response = make_response(render_template('./profile.html'))
        response.set_cookie('activeUser', session_id)
        return response


@app_views.route('/logout', methods=['POST'], strict_slashes=False)
def logout():
    pass
