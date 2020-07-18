#!/usr/bin/env python3
"""
Top level API routes
"""
from flask import jsonify, abort, render_template, request, redirect
from api.v1.views import app_views
from api.v1.views.auth.auth import Auth
from models import User


auth = Auth()

@app_views.route('/me', methods=['GET'], strict_slashes=False)
def user_page():
    session = auth.session_cookie(request)
    if not session:
        return redirect('./auth/login.html')
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


@app_views.route('/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
def home():
    """
    -----------------------------
    Check request method and validate user if needed.
    -----------------------------
    -> Return: Public landing page or login redirect page.
    """
    print('in views')
    from flask import make_response
    pics = ['static/images/team_member_1.jpg', 'static/images/team_member_2.jpg', 'static/images/team_member_3.jpg', 'static/images/team_member_1.jpg', 'static/images/team_member_2.jpg', 'static/images/team_member_3.jpg', 'static/images/team_member_1.jpg', 'static/images/team_member_2.jpg', 'static/images/team_member_3.jpg']
    if request.method == "GET":
        session_id = request.cookies.get('activeUser')
        if request.cookies.get('debug'):
            return render_template('./index.html',  session=session_id, pics=pics)
        from models import db
        users = User.search()
        return render_template('./index.html', all_users=users, session=session_id, pics=pics)
    elif request.method == "POST":
        email, pwd = request.form.get('email'), request.form.get('password')
        # validate_user returns a userJson if True and ErrorMessage if False.
        user_or_error = auth.validate_user(email, pwd)
        print(email, pwd)
        if not type(user_or_error) == User:
            users = User.search()
            return render_template('./index.html', debug=user_or_error, all_users=users, pics=pics)
        user = user_or_error
        session_id = auth.create_session(user.id)
        users = User.search()
        res = make_response(render_template('./index.html', session=session_id, debug='signed in as ' + user.username, all_users=users, pics=pics))
        res.set_cookie('activeUser', session_id)
        return res


@app_views.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == "GET":
        print("IN HERE")
        return render_template('./auth/register.html')
    if request.method == "POST":
        print("IN HERE YO")
        username = request.form.get('username')
        email = request.form.get('email')
        pwd = request.form.get('password')
        user = User()
        user.username = username
        user.email = email
        user.password = pwd
        print(user.password)
        user.save_to_db()
        for k, v in user.__dict__.items():
            print(k, v)
        users = User.search()
        pics = ['static/images/team_member_1.jpg', 'static/images/team_member_2.jpg', 'static/images/team_member_3.jpg', 'static/images/team_member_1.jpg', 'static/images/team_member_2.jpg', 'static/images/team_member_3.jpg', 'static/images/team_member_1.jpg', 'static/images/team_member_2.jpg', 'static/images/team_member_3.jpg']
        return render_template('./index.html', debug=f'{user.username} has been registered!', all_users=users, pics=pics)


@app_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template('./auth/login.html')
    return redirect('/')


@app_views.route('/logout', methods=['POST'], strict_slashes=False)
def logout():
    pass
