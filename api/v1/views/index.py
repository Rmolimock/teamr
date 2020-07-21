#!/usr/bin/env python3
"""
Top level API routes
"""
from flask import jsonify, abort, render_template, request, redirect, make_response
from api.v1.views import app_views
from api.v1.views.auth.auth import Auth
from models import User
from models.nav_link import *


auth = Auth()

@app_views.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """
    -----------------------------
    Check if logged in and render landing page.
    -----------------------------
    -> Return: Public landing page.
    """
    users = User.search()
    session = request.cookies.get('activeUser')
    user = get_user_from_session(request)
    if not user:
        # public home page
        return render_template('./index.html',
                                all_users=users,
                                nav_links=home_pub_links,
                                nav_buttons=home_pub_buttons)
    # if user is logged in display dashboard
    home_private_buttons[0].url = user.profile_url
    return render_template('./index.html',
                            all_users=users,
                            session_id=session,
                            profile_url=user.profile_url,
                            nav_links=home_private_links,
                            nav_buttons=home_private_buttons)


@app_views.route('/users/<user_id>', methods=['GET', 'POST'], strict_slashes=False)
def user_page(user_id=None):
    """
    ----------------------------
    Profile page of the current user.
    ----------------------------
    -> Return: Profile.html with private fields.
    """
    if request.method == 'GET':
        user = get_user_from_session(request)
        if not user:
            return redirect('./auth/login.html')
        if user_id == user.id:
            """
            user is visiting their own profile page
            """
            user_dict = user.to_json()
            return render_template('./profile.html',
                                    auth_user=user_dict,
                                    nav_links=profile_private_links,
                                    nav_buttons=profile_private_buttons)
        else:
            from models import User
            user = User.search({'id': user_id})
            if not user:
                abort(404)
            """
            user is visiting the profile page of someone else
            """
            user_dict = user[0].to_json()
            return render_template('./profile.html',
                                    pub_user=user_dict,
                                    nav_links=profile_private_links,
                                    nav_buttons=profile_private_buttons)
    elif request.method == 'POST':
        from models import db
        pwd1 = request.form.get('new_password1')
        pwd2 = request.form.get('new_password2')
        if not pwd1 or not pwd2 or not pwd1 == pwd2:
            return render_template('./auth/reset_password.html', msg="Passwords are not a match. Try again.")
        session = request.cookies.get('activeUser')
        user_id = auth.user_id_for_session_id(session) 
        user_id = {'id': user_id}
        user = User.search(user_id)
        if not user:
            abort(401)
        user = user[0]
        new_password = db.hash_password(pwd1)
        user.password = new_password
        user.save_to_db()
        return render_template('./profile.html', user=user.to_json(), msg="Password updated.")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    ----------------------------
    Check the status of the API.
    ----------------------------
    -> Return: Json response with status message "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    -----------------------------
    Check request method and register user if acceptable credentials.
    -----------------------------
    -> Return: Profile page if successful, otherwise /register with error.
    """
    from validate_email import validate_email
    from models import db
    if request.method == "GET":
        return render_template('./auth/register.html',
                                nav_links=register_links,
                                nav_buttons=register_buttons)
    if request.method == "POST":
        uname = request.form.get('username')
        email = request.form.get('email')
        pwd = request.form.get('password')
        user = db.register(uname, email, pwd)
        if not type(user) == User or not validate_email(email):
            return render_template('./auth/register.html',
                                    msg=user,
                                    nav_links=register_links,
                                    nav_buttons=register_buttons)
        session_id = auth.create_session(user.id)
        response = make_response(render_template('./profile.html',
                                                  auth_user=user,
                                                  nav_links=profile_private_links,
                                                  nav_buttons=profile_private_buttons))
        response.set_cookie('activeUser', session_id)
        return response


@app_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    -----------------------------
    Check request method and verify user credentials if POST.
    -----------------------------
    -> Return: Profile page if successful, otherwise /login with error.
    """
    from validate_email import validate_email
    # 
    if request.method == 'GET':
        return render_template('./auth/login.html',
                                nav_links=login_links,
                                nav_buttons=login_buttons)
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        if not validate_email(email):
            return render_template('./auth/login.html',
                                    msg='Please enter a valid email address.',
                                    nav_links=login_links,
                                    nav_buttons=login_buttons)
        user_or_error = auth.validate_user(email, pwd)
        if not type(user_or_error) == User:
            return render_template('./auth/login.html',
                                    msg=user_or_error,
                                    nav_links=login_links,
                                    nav_buttons=login_buttons)
        user = user_or_error
        session_id = auth.create_session(user.id)
        response = make_response(render_template('./index.html',
                                                  auth_user=user.to_json(),
                                                  profile_url=user.profile_url,
                                                  nav_links=home_private_links,
                                                  nav_buttons=home_private_buttons))
        response.set_cookie('activeUser', session_id)
        return response
        

@app_views.route('/logout', methods=['POST', 'GET', 'DELETE'], strict_slashes=False)
def logout():
    """
    -----------------------------
    Delete current session cookie if present.
    -----------------------------
    -> Return: Public landing page.
    """
    msq = 'Logged out.'
    user = get_user_from_session(request)
    if not user:
        return redirect('./auth/login.html',
                         nav_links=login_links,
                         nav_buttons=login_buttons)
    auth.destroy_session(request)
    return redirect('/')


@app_views.route('/reset_password', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/reset_password/<token>', methods=['GET', 'POST'], strict_slashes=False)
def reset_password(token=None):
    """
    -----------------------------
    Check request method and send reset token if POST.
    -----------------------------
    -> Return: reset.html with confirmation message.
    """
    if request.method == 'GET' and token == None:
        return render_template('./auth/forgot_password.html')
    elif request.method == 'POST' and token == None:
        import os
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        from uuid import uuid4
        email = request.form.get('email')
        token = str(uuid4())
        auth.reset_password_tokens[token] = email
        message = Mail(
            from_email='support@thepointistochangeit.com',
            to_emails=email,
            subject='Teamr password reset.',
            html_content='<a href="https://www.thepointistochangeit.com/reset_password/' + token + '">Click here to reset your Teamr password.</a>')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            # in the future, log these messages instead of printing
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
        return render_template('./auth/forgot_password.html', msg="A link has been sent to the email address provided.")
    elif token:
        from models import User
        if not token in auth.reset_password_tokens:
            return render_template('./auth/forgot_password.html', msg="Reset token expired. Enter your email again.")
        email = auth.reset_password_tokens[token]
        email = {'email': email}
        user = User.search(email)
        if not user:
            return render_template('./auth/register.html', msg="No account is associated with this email. Please register.")
        user = user[0]
        session_id = auth.create_session(user.id)
        print(session_id)
        response = make_response(render_template('./auth/reset_password.html', user=user.to_json()))
        response.set_cookie('activeUser', session_id)
        del auth.reset_password_tokens[token]
        return response



"""
----------------
HELPER FUNCTIONS
----------------
"""


def get_user_from_session(request):
    """
    ----------------------------
    Check for a user associated with the current session
    ----------------------------
    -> Return: User
    """
    session = auth.session_cookie(request)
    print(session)
    user_id = auth.current_user(session)
    print(user_id)
    user = User.get(user_id)
    print(user)
    return user