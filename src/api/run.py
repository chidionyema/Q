# from gevent import monkey
# monkey.patch_all()
import eventlet
eventlet.monkey_patch(socket=True, select=True)

# Python built-ins
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import Counter
import concurrent.futures
import logging
import os
import time
import requests

import traceback

# Third-party libraries
from flask import Flask, session, request, make_response, jsonify, redirect, abort, url_for
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_cors import CORS
from flask_limiter import Limiter
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_oauthlib.client import OAuth

from flask_socketio import SocketIO, emit 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import jwt
import secrets
from app.tasks import train_model_task
from validate_email import validate_email
from functools import wraps
from app.engine import Pipeline2, RandomForest, DataLoader
from app import socketio, db
from app.dbdata import User, PasswordResetToken, TaskResult

load_dotenv()

# Access environment variables
secret_key = os.environ.get('SECRET_KEY')
database_uri = os.environ.get('DATABASE_URI')
base_uri = os.environ.get('BASE_URI')
jwt_secret = os.environ.get('JWT_SECRET')
sql_alchemy_track_modifications = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
flask_app = os.environ.get('FLASK_APP')
flask_env = os.environ.get('FLASK_ENV')

from app import app
#app = create_app()
app.debug = True
app.logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
app.logger.addHandler(handler)

app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'


# Flask app configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'false').lower() == 'true'
app.config['BASE_URI'] = os.environ.get('BASE_URI')

# SSL Certificates path
app.config['CERT_PATH'] = os.environ.get('CERT_PATH')
app.config['KEY_PATH'] = os.environ.get('KEY_PATH')
app.logger.setLevel(logging.INFO)  # or logging.DEBUG

oauth = OAuth(app)
CORS(app, resources={r"/*": {
    "origins": "https://ui.dev.io:3000",
    "supports_credentials": True,
    "allow_headers": ["Content-Type", "Authorization"]
}})

limiter = Limiter(app)
# If you're using multiple instances or servers, make sure that each one of them has access to this Redis server.


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#cert_path = os.environ.get('CERT_PATH')
#key_path = os.environ.get('KEY_PATH')


bcrypt = Bcrypt(app)
JWT_SECRET = os.environ.get('JWT_SECRET')

migrate = Migrate(app, db) 



def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated_function
   
            
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500



@app.route('/reset_password', methods=['GET', 'POST'])
def request_password_reset():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a password reset token
            reset_token = generate_reset_token()
            expiration_time = datetime.utcnow() + timedelta(seconds=app.config['PASSWORD_RESET_EXPIRATION'])
            token_entry = PasswordResetToken(token=reset_token, user_id=user.id, expiration_time=expiration_time)
            db.session.add(token_entry)
            db.session.commit()

            # Send a password reset email asynchronously using Celery
            reset_link = url_for('reset_password', token=reset_token, _external=True)
            send_password_reset_email.apply_async(args=[email, reset_link])

            flash("Password reset email sent. Check your email for instructions.", 'success')
            return redirect(url_for('login'))
        else:
            flash("Email not found. Please register.", 'danger')
            return redirect(url_for('register'))

    return render_template('reset_password.html')

@app.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    token_entry = PasswordResetToken.query.filter_by(token=token).first()

    if not token_entry:
        flash("Invalid or expired reset token.", 'danger')
        return redirect(url_for('login'))

    if datetime.utcnow() > token_entry.expiration_time:
        # Token has expired
        db.session.delete(token_entry)
        db.session.commit()
        flash("The reset token has expired. Please request a new one.", 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')

        if len(new_password) < 8:
            flash("Password should be at least 8 characters long.", 'danger')
        else:
            user = User.query.get(token_entry.user_id)
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.delete(token_entry)
            db.session.commit()
            flash("Password reset successful. You can now log in with your new password.", 'success')
            return redirect(url_for('login'))

    return render_template('reset_password_form.html')

def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Print statements for debugging
    print("Received POST request to /register")
    print(f"Email: {email}")
    print(f"Password: {password}")

    if not validate_email(email):
        print("Invalid email format!")
        return jsonify({"message": "Invalid email format!"}), 400
    if len(password) < 8:
        print("Password is too short!")
        return jsonify({"message": "Password should be at least 8 characters!"}), 400

    user = retrieve_or_create_user(email, "", "")

    token = generate_jwt_token_for_user(user)

    # Print statements for debugging
    print("User registered successfully")
    print(f"Generated JWT Token: {token}")

    # Return both the token and the email
    return jsonify({"token": token, "email": email})



@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # Create a token or session logic here
        token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)}, JWT_SECRET, algorithm='HS256')
        return jsonify({"token": token, "email": email})
    return jsonify({"message": "Invalid credentials!"}), 401


google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=os.environ.get('FACEBOOK_APP_ID'),
    consumer_secret=os.environ.get('FACEBOOK_APP_SECRET'),
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
)

@google.tokengetter
def get_google_token(token=None):
    return session.get('google_token')

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')



BASE_URL = os.environ.get('NEXTAUTH_URL')
REDIRECT_URI = "https://api.dev.io:5000/login/google/authorized"



@app.route('/login/google')
def login_google():

    print("Start of login_google")
    print(f"Request headers: {request.headers}")

    try:
        state = os.urandom(16).hex()  # Generate a random state value
        print(f"Generated state: {state}")

        session['oauth_state'] = state  # Store it in user's session
        print("Stored state in session")

        # Always initiate Google's OAuth process with forcing consent
        # Add the access_type and prompt parameters here
        return_val = google.authorize(
            callback=REDIRECT_URI, 
            state=state, 
            prompt='consent',
            access_type='offline'  # Specify that you want offline access
        )
        
        print("Initiated Google's OAuth process with consent prompt")
        return return_val

    except Exception as e:
        logging.error(f"Unexpected error in login_google: {e}")
        return jsonify({"error": "An unexpected error occurred during login."}), 500

    # This line seems redundant as you already have a return statement inside the try block
    # So, you can safely remove the following line:
    # return google.authorize(callback=REDIRECT_URI, state=state, prompt='consent')




@app.route('/token/refresh', methods=['POST'])
@token_required
def refresh_token(current_user):
    # Get the refresh token for the current user from your database
    refresh_token_stored = get_refresh_token_for_user(current_user)

    # If no refresh token is stored, ask the user to authenticate again
    if not refresh_token_stored:
        # Depending on your frontend design, you can send a specific error code or message
        return jsonify({"error": "Refresh token not available. Please authenticate again."}), 401

    # Prepare the payload to request a new access token from Google using the refresh token
    token_payload = {
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'refresh_token': refresh_token_stored,
        'grant_type': 'refresh_token'
    }

    # Request a new access token from Google's token endpoint
    response = requests.post("https://oauth2.googleapis.com/token", data=token_payload)
    response_data = response.json()

    if 'error' in response_data:
        # Handle the error, maybe redirect the user to login again or return an error response
        return jsonify({"error": response_data['error_description']}), 400

    # If Google provides a new refresh token, update it in your database
    new_refresh_token = response_data.get('refresh_token')
    if new_refresh_token:
        update_refresh_token_for_user(current_user, new_refresh_token)

    # Generate a new JWT token for the user
    token = jwt.encode({
        'user_id': current_user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, JWT_SECRET, algorithm='HS256')
    
    return jsonify({"token": token}), 200

def is_token_close_to_expiry(token):
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    expiration_time = decoded_token.get("exp")
    buffer_time = 10 * 60  # 10 minutes
    current_time = time.time()
    return (expiration_time - current_time) < buffer_time


def get_refresh_token_for_user(user):
    """
    Fetches the refresh token for a given user from the database.
    
    Args:
        user: The user object for which to fetch the refresh token.
        
    Returns:
        str: The refresh token for the given user.
        None: If the user doesn't have a stored refresh token.
    """
    # Fetch the user from the database
    db_user = User.query.filter_by(id=user.id).first()

    # If the user exists and has a refresh_token attribute, return it.
    if db_user and hasattr(db_user, 'refresh_token'):
        return db_user.refresh_token
    
    # Otherwise, return None
    return None


import logging
from flask import jsonify

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.delete_cookie('auth_token')
    return response



@app.route('/login/google/authorized')
def authorized_google():
    print("Start of authorized_google")
    try:
        # Capture the state
        state_from_callback = request.args.get('state')
        state_from_session = session.get('oauth_state')
        print(f"State from callback: {state_from_callback}")
        print(f"State from session: {state_from_session}")

        # Check state
        if not state_from_callback or state_from_callback != state_from_session:
            logging.error("State mismatch error. Possible CSRF attack.")
            raise ValueError("State mismatch error. Possible CSRF attack.")
        
        # Capture the authorization code
        authorization_code = request.args.get('code')
        print(f"Authorization code: {authorization_code}")
        if not authorization_code:
            logging.error("Authorization code is missing!")
            raise ValueError("Authorization code is missing!")

        # Set token endpoint and prepare payload
        token_endpoint = "https://oauth2.googleapis.com/token"
        payload = {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'redirect_uri': os.environ.get('REDIRECT_URI')
        }
        print("Sending request to Google's token endpoint")

        # Get response from Google's token endpoint
        response = requests.post(token_endpoint, data=payload)
        response_data = response.json()

        print(f"Response from Google's token endpoint: {response_data}")

        if 'error' in response_data:
            logging.error(f"Error in response_data: {response_data['error_description']}")
            raise ValueError(response_data['error_description'])

        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')
        print(f"Access token: {access_token}")
        print(f"Refresh token: {refresh_token}")

        if not access_token:
            logging.error("Failed to obtain access token from Google!")
            raise ValueError("Failed to obtain access token from Google!")

        user_info = fetch_user_info_from_google(access_token)
        email = user_info["email"]
        user = retrieve_or_create_user(email, access_token, refresh_token)

        print(f"User info: {user_info}")
        print(f"User object: {user}")

        if not user:
            logging.error("Failed to retrieve or create user.")
            raise ValueError("Failed to retrieve or create user.")
  


        token = generate_jwt_token_for_user(user)
        print("generated new jwt token")

        # Enhancing security of cookies and setting expiration
        expiration_time = datetime.now() + timedelta(days=1)  # 1 day expiration for example
        # Replace 'YOUR_CALLBACK_URL' with the actual callback URL
        callback_url = 'https://ui.dev.io:3000/callback' + f'?token={token}'
        print("set callback and sending back response")

        if user.is_active == False:
            activation_token = generate_activation_token()
        # Send an email with the activation link asynchronously
            activation_link = url_for('activate_account', token=activation_token, _external=True)
            #send_activation_email.apply_async(args=[email, activation_link])


        response = make_response(redirect(callback_url))
        response.set_cookie(
            'auth_token', 
            token, 
            httponly=True, 
            secure=True, 
            samesite='None', 
            expires=expiration_time,
            domain=".dev.io"  # <-- Set the domain attribute here
        )

        headers = response.headers
        print(f"Headers from Google's token endpoint: {headers}")

        print("Returning successful response.")

        return response


    except ValueError as e:
        logging.error(f"Value Error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
   
        return jsonify({"error": "An unexpected error occurred."}), 500

# Example user activation logic
@app.route('/activate_account/<string:token>', methods=['GET'])
def activate_account(token):
    # Check if the token is valid (you may have your own token validation logic)
    if True:
        # Activate the user's account (you may have your own activation logic)
        #  activate_user(token)
        flash("Account activated successfully!", 'success')
        return redirect(url_for('login'))  # Redirect to the login page
    else:
        flash("Invalid or expired activation token.", 'danger')
        return redirect(url_for('login'))  # Redirect to the login page with an error message


def generate_activation_token():
    # Generate a random token using the secrets module
    activation_token = secrets.token_hex(16)  # You can adjust the token length as needed
    return activation_token



def error_response(message, status_code=400):
    print(message)
    return jsonify({"message": message}), status_code

def retrieve_or_create_user(email, access_token, refresh_token, provider="google"):
    # Assuming you have a User model with attributes email, name, access_token, refresh_token, provider, etc.
    user = User.query.filter_by(email=email).first()
    if not user:
        # Create new user
        user = User(
            email=email,  # Use the provided email parameter
            name=email,  # Use the provided email as the name (you can modify this as needed)
            access_token=access_token,
            is_active=False,
            refresh_token=refresh_token,
            provider=provider  # Setting the provider here
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update the tokens for the existing user
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.provider = provider  # Updating the provider, though in many use-cases, this might remain unchanged
        db.session.commit()

    return user




def fetch_user_info_from_google(access_token):
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    userinfo_response = requests.get(userinfo_url, params={'access_token': access_token})
    return userinfo_response.json()


def get_or_create_user(email, name=None, provider=None, provider_id=None):
   
    user = User(email=email, name=name, provider=provider, provider_id=provider_id)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
     # handle/log exception
    return user


def generate_jwt_token_for_user(user):
    return jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'nbf': datetime.utcnow()
    }, JWT_SECRET, algorithm='HS256')

@app.route('/auth/login', methods=['POST'])
def custom_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    
    # Assuming you have some function to validate the password
    if not user or not validate_password(user, password):
        return error_response("Invalid credentials")

    token = generate_jwt_token_for_user(user)
    return jsonify({"token": token, "user": {"name": user.name, "email": user.email}})


@app.route('/login/facebook/authorized')
def authorized_facebook():
    response = facebook.authorized_response()

    if response is None or response.get('access_token') is None:
        return jsonify({"message": "Access denied!"}), 403

    session['facebook_token'] = (response['access_token'], '')
    user_info = facebook.get('/me?fields=id,email,name').data

    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = get_or_create_user(user_info['email'], user_info['name'], "facebook", user_info['id'])

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'nbf': datetime.utcnow()
    }, JWT_SECRET, algorithm='HS256')


    return jsonify({"token": token, "user": {"name": user.name, "email": user.email}})


@app.route('/some_protected_route')
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Hello {current_user.name}"})

# Caching configuration (adjust cache_timeout as needed)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  # Cache for 1 hour

# Import caching extension and initialize it
from flask_caching import Cache
cache = Cache(app)

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None


# Route to fetch JSON data
@app.route('/fetch-models', methods=['GET'])
@cache.cached()  # Cache the response
def fetch_models():
    data = load_json_data('data/nod_attr.json')

    if data is not None:
        return jsonify(data)
    else:
        return jsonify({'error': 'JSON file not found'}), 404

# Route to fetch JSON data
@app.route('/fetch_ensembles', methods=['GET'])
@cache.cached()  # Cache the response
def fetch_ensembles():
    data = load_json_data('data/ens_attr.json')

    if data is not None:
        return jsonify(data)
    else:
        return jsonify({'error': 'JSON file not found'}), 404

# Route to fetch JSON data
@app.route('/fetch_optimizers', methods=['GET'])
@cache.cached()  # Cache the response
def fetch_optimizers():
    data = load_json_data('data/opt_attr.json')

    if data is not None:
        return jsonify(data)
    else:
        return jsonify({'error': 'JSON file not found'}), 404


VALID_MODEL_TYPES = ["random_forest", "linear_regression"]  # Add all valid model types here
import logging

@socketio.on('train_model')
def handle_train_model_event(data):
    symbol = data.get('symbol')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    model = data.get('model')

    # Log the event and data
    logging.info(f'Received train_model event with data: {data}')

    try:
        # Trigger the Celery task asynchronously
        task = train_model_task.delay(symbol, start_date, end_date, model)

        # Emit a message to the client
        emit('training_started', {'message': 'Training has started'})

        # Log the task details
        logging.info(f'Training task started: Task ID={task.id}, Symbol={symbol}, Model={model}')

    except Exception as e:
        # Handle exceptions gracefully and log errors
        logging.error(f'Error starting training task: {str(e)}')
        emit('training_error', {'error_message': str(e)})

@app.route('/startTraining', methods=['POST'])
@limiter.limit("5 per minute")
def start_training():
    try:
        data = request.json
        symbol = data.get("symbol")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        model = data.get("model")

        # Logging: Log the incoming data
        logging.info(f"Received data: {data}")

        # Check for valid model type
       # if model not in VALID_MODEL_TYPES:
      #      return jsonify({'error': 'Invalid model type'}), 400

        # Basic data validation (extend as necessary)
        if not all([symbol, start_date, end_date, model]):
            error_message = 'Missing or invalid data'
            # Logging: Log the error message
            logging.error(error_message)
            return jsonify({'error': error_message}), 400
        
        # Launch the Celery task
        task = train_model_task.delay(symbol, start_date, end_date, model)

        # Logging: Log the task ID and status
        logging.info(f"Task ID: {task.id}, Status: Training started")

        # Return the task ID to the client, which they can use to query the status and results later
        return jsonify({'status': 'Training started', 'task_id': task.id}), 202

    except Exception as e:
        # Logging: Log the exception
        logging.exception("An exception occurred")
        # Send error message to client
        return jsonify({'error': str(e)}), 500

import uuid

def generate_unique_id():
    # Generate a unique identifier using UUID
    return str(uuid.uuid4())



@socketio.on('connect', namespace='/training')
def connect():
    print("Client connected")
    emit('progress', {'progress': 'Connection established'})

@socketio.on('disconnect', namespace='/training')
def disconnect():
    print("Client disconnected")


if __name__ == '__main__':
    # Use the absolute paths in the ssl_context parameter
     socketio.run(app, debug=True, host='0.0.0.0', port=5000, keyfile='./api.dev.io.key', certfile='./api.dev.io.crt')




