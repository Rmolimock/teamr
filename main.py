#!/usr/bin/env python3
"""
Route module for the API
"""
# this is the new one
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_cors import (CORS, cross_origin)
from flask import jsonify, Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import os
<<<<<<< HEAD
from models.nav_link import *
# from api.v1.views import app_views
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

=======
# from api.v1.views import app_views
>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c




# instantiate the app, add cors protection, and check which authentication
# method it should run with.
app = Flask(__name__)
# app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
import secrets
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
print(app.secret_key)
<<<<<<< HEAD

"""
----------------------------
Flask-login setup
----------------------------
"""
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
# login_manager.login_view = redirect on bad login
@login_manager.user_loader
def load_user(user_id):
    """
    Tell Flask-Login how to find a specific user
    from the ID that is stored in the session cookie.
    """
    return User.get(user_id)


"""
----------------------------
Authentication Routes
----------------------------
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
=======

"""
----------------------------
Flask-login setup
----------------------------
"""
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
# login_manager.login_view = redirect on bad login
@login_manager.user_loader
def load_user(user_id):
    """
    Tell Flask-Login how to find a specific user
    from the ID that is stored in the session cookie.
    """
    return User.get(user_id)
>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        register_buttons[0].url = url_for('login')
        return render_template('auth/register.html',
                                nav_buttons=register_buttons)
    # post request
    from validate_email import validate_email
    # get info from the registration form
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    # check if the email is already in use
    existing_user = User.search({'email': email})
    if existing_user:
        print('Email is already in use.')
        flash('Email is already in use.')
        return redirect('/register')
    # check if the password is strong enough
    if not password_check(password)[0]:
        password_error = ''
        for k,v in password_check(password)[1].items():
            if v:
                password_error += k
        flash(password_error)
        return redirect('/register')
    response = bad_uploaded_file(request)
    if response:
        print('file not ok')
        return redirect('/register')
    user_info = {
                'email': email,
                'password': generate_password_hash(password, method='sha256'),
                'username': username
                }
    user = User(**user_info)
    save_profile_picture(file, user)
    user.save_to_db()
    flash(f'Welcome {username}!')
    login_user(user)
    return redirect(url_for('profile'))

<<<<<<< HEAD
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.search({'email': email})
    user = user[0] if user else None
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('profile'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))







=======
"""
----------------------------
Authentication Routes
----------------------------
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    # post request
    from validate_email import validate_email
    # get info from the registration form
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    # check if the email is already in use
    existing_user = User.search({'email': email})
    if existing_user:
        print('email in use')
        flash('Email is already in use.')
        return redirect('/register')
    # check if the password is strong enough
    if not password_check(password)[0]:
        password_error = ''
        for k,v in password_check(password)[1].items():
            if v:
                password_error += k
        flash(password_error)
        return render_template('./auth/register.html')
    response = bad_uploaded_file(request)
    if response:
        print('file not ok')
        flash('Profile picture must be one of these formats: .png, .jpg, .jpeg, or .bmp')
        return render_template('./auth/register.html')
    user_info = {
                'email': email,
                'password': generate_password_hash(password, method='sha256'),
                'username': username
                }
    user = User(**user_info)
    user.save_to_db()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.search({'email': email})
    user = user[0] if user else None
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('profile'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c

"""
----------------------------
Helper functions.
----------------------------
"""
def bad_uploaded_file(request):
    image_formats = ['png', 'jpg', 'jpeg', 'bmp']
    if 'file' not in request.files:
        print(1)
<<<<<<< HEAD
        flash('Profile picture required.')
=======
>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c
        return True
    file = request.files['file']
    if file.filename == '' or not '.' in file.filename:
        print(2)
<<<<<<< HEAD
        flash('Profile picture required.')
=======
>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c
        return True
    if file.filename.split('.')[-1:][0] not in image_formats:
        print(3)
        print(file.filename.split('.')[-1:][0])
<<<<<<< HEAD
        flash('Profile picture must be one of these formats: .png, .jpg, .jpeg, or .bmp')
=======
>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c
        return True
    return False

def password_check(password):
<<<<<<< HEAD
    """
    Verify the strength of 'password'
    Returns a dict indicating the incorrect criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """
    import re
    # checking the length
    length_error = len(password) < 8
    # searching for digits
    digit_error = re.search(r"\d", password) is None
    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None
    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None
    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
    return (password_ok,
            {
            'Password must contain: ': 1,
            'at least 8 characters, ' : length_error,
            'a number, ' : digit_error,
            'an uppercase letter, ' : uppercase_error,
            'a lowercase letter, ' : lowercase_error,
            'a symbol.' : symbol_error,
            })

def save_profile_picture(file, user):
    if file and allowed_file(file.filename):
        ext = secure_filename(file.filename).split('.')[-1:][0].lower()
        filename = user.id + '.' + ext
        file.save(os.path.join(os.path.dirname(__file__) + '/../../../' + os.path.join(f"static/images/users", filename)))
        user.image += ext
        user.save_to_db()


@app.route('/tokensignin', methods=['POST'], strict_slashes=False)
def google_signin_token():
    token = request.form.getlist('idtoken')[0]
    from google.oauth2 import id_token
    from google.auth.transport import requests
    # (Receive token by HTTPS POST)
    # ...
    try:
        
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        print('userid = ', userid)
    except ValueError:
        # Invalid token
        print('invalid')
        pass
    return redirect('/users')







"""
----------------------------
Status checks
----------------------------
"""
@app.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    ----------------------------
    Check the status of the API.
    ----------------------------
    -> Return: Json response with status message "OK"
    """
    return jsonify({"status": "OK"})
=======
    """
    Verify the strength of 'password'
    Returns a dict indicating the incorrect criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """
    import re
    # checking the length
    length_error = len(password) < 8
    # searching for digits
    digit_error = re.search(r"\d", password) is None
    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None
    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None
    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
    return (password_ok,
            {
            'password ': 1,
            'is too short, ' : length_error,
            'must contain a number, ' : digit_error,
            'must contain an uppercase letter, ' : uppercase_error,
            'must contain a lowercase letter, ' : lowercase_error,
            'must contain a symbol.' : symbol_error,
            })
        
>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c

@app.route('/register_old', methods=['GET', 'POST'])
def register_old():
    if request.method == 'GET':
        print('request is get')
        return render_template('./auth/register.html')
    if request.method == 'POST':
        print('request is post')
        
        file = request.files['file']
        user_name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.register(user_name, email, password)
        if not type(user) == User or not 1:
            print('error message')
            return render_template('./auth/register.html')
        login_user(user)
        print('registered')
        return render_template('./index.html')

<<<<<<< HEAD
=======
@app.route('/tokensignin', methods=['POST'], strict_slashes=False)
def google_signin_token():
    token = request.form.getlist('idtoken')[0]
    from google.oauth2 import id_token
    from google.auth.transport import requests
    # (Receive token by HTTPS POST)
    # ...
    try:
        
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        print('userid = ', userid)
    except ValueError:
        # Invalid token
        print('invalid')
        pass
    return redirect('/users')











>>>>>>> 258a2630e62d2286eb303e12687ccb41ff0a336c
"""
----------------------------
Error responses
----------------------------
"""
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
    host = os.getenv("API_HOST", "127.0.0.1")
    port = os.getenv("API_PORT", "8080")
    app.run(host=host, port=port)
