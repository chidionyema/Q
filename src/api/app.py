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
from flask_oauthlib.client import OAuth
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import jwt
from validate_email import validate_email
from functools import wraps
from engine import Pipeline2, RandomForest, DataLoader


load_dotenv()

# Access environment variables
secret_key = os.environ.get('SECRET_KEY')
database_uri = os.environ.get('DATABASE_URI')
base_uri = os.environ.get('BASE_URI')
jwt_secret = os.environ.get('JWT_SECRET')
sql_alchemy_track_modifications = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
flask_app = os.environ.get('FLASK_APP')
flask_env = os.environ.get('FLASK_ENV')



app = Flask(__name__)

app.debug = True
app.logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
app.logger.addHandler(handler)


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


socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cert_path = os.environ.get('CERT_PATH')
key_path = os.environ.get('KEY_PATH')


bcrypt = Bcrypt(app)
JWT_SECRET = os.environ.get('JWT_SECRET')

migrate = Migrate(app, db) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)  # It's good to ensure this is securely hashed if you use it
    name = db.Column(db.String(120), nullable=True)
    provider = db.Column(db.String(50), nullable=True)
    provider_id = db.Column(db.String(120), unique=True, nullable=True)
    access_token = db.Column(db.String(500), nullable=True)
    refresh_token = db.Column(db.String(500), nullable=True)
    first_login = db.Column(db.Boolean, default=True, nullable=True)



    def __repr__(self):
            return f"<User {self.email}>"    

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

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
   
    if not validate_email(email):
        return jsonify({"message": "Invalid email format!"}), 400
    if len(password) < 8:
        return jsonify({"message": "Password should be at least 8 characters!"}), 400

    user = retrieve_or_create_user(email, "", "")

    token = generate_jwt_token_for_user(user)

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
        return jsonify({"message": "Logged in!", "token": token}), 200
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
  

         # If not their first login or after handling the first login
        token = generate_jwt_token_for_user(user)
        print("generated new jwt token")

        # Enhancing security of cookies and setting expiration
        expiration_time = datetime.now() + timedelta(days=1)  # 1 day expiration for example
        # Replace 'YOUR_CALLBACK_URL' with the actual callback URL
        callback_url = 'https://ui.dev.io:3000/callback' + f'?token={token}'
        print("set callback and sending back response")

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


@app.route('/startTraining', methods=['POST'])
def start_training():
    try:
        data = request.json
        symbol = data.get("symbol")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        model = data.get("model")

        # Basic data validation (extend as necessary)
        if not all([symbol, start_date, end_date, model]):
            abort(400, "Missing or invalid data")

        # Validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")

        # Ensure the symbol is valid (add more validation if needed)
        if not symbol_is_valid(symbol):
            abort(400, "Invalid symbol")

        # Rest of your code...
        
        # Sample usage of model builder and optimizer
        rf_builder = ModelBuilder(RandomForestRegressor, optimizer=GridSearchOptimizer(param_grid={"n_estimators": [10, 50, 100]}))

        # Sample usage of the data processing pipeline
        stocks_info = [(symbol, start_date, end_date, 14, 3, rf_builder)]
        pipeline = Pipeline2(stocks_info)
        predictions = pipeline.process_data_pipeline()

        mae_values = []  # Store MAE values to send to the client

        for prediction in predictions:
            si, test_predictions, mae_val, mae_test = prediction
            mae_values.append({'mae_val': mae_val, 'mae_test': mae_test})

        return jsonify({'status': 'Training completed', 'mae_values': mae_values}), 202

    except ValueError as ve:
        app.logger.error("ValueError: %s", str(ve))
        return jsonify({'error': 'Invalid date format.'}), 400
    except Exception as e:
        app.logger.error("An error occurred: %s", str(e))
        return jsonify({'error': 'An error occurred.'}), 500


    except Exception as e:
        # Send error message to client
        return jsonify({'error': str(e)}), 500


@socketio.on('connect', namespace='/training')
def connect():
    print("Client connected")
    emit('progress', {'progress': 'Connection established'})

@socketio.on('disconnect', namespace='/training')
def disconnect():
    print("Client disconnected")


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, ssl_context=('./api.dev.io.key', './api.dev.io.crt'))



