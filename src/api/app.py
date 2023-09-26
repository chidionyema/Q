# Python built-ins
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import Counter
import concurrent.futures
import logging
import os
import time
import traceback

# Third-party libraries
from flask import Flask, jsonify, request, abort, redirect, url_for, session
from flask_bcrypt import Bcrypt
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


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Flask app configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'false').lower() == 'true'
app.config['BASE_URI'] = os.environ.get('BASE_URI')

# SSL Certificates path
app.config['CERT_PATH'] = os.environ.get('CERT_PATH')
app.config['KEY_PATH'] = os.environ.get('KEY_PATH')

oauth = OAuth(app)
CORS(app, origins=[os.environ.get('BASE_URI')])


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
    password = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    provider = db.Column(db.String(50), nullable=True)
    provider_id = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
            return f"<User {self.email}>"    



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
   
    if not validate_email(email):
        return jsonify({"message": "Invalid email format!"}), 400
    if len(password) < 8:
        return jsonify({"message": "Password should be at least 8 characters!"}), 400
 
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered!"}), 201

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

@app.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('authorized_google', _external=True))

@app.route('/login/facebook')
def login_facebook():
    return facebook.authorize(callback=url_for('authorized_facebook', _external=True))

@app.route('/login/google/authorized')
def authorized_google():
    response = google.authorized_response()

    if response is None or response.get('access_token') is None:
        return jsonify({"message": "Access denied!"}), 403

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo').data

    user = User.query.filter_by(email=user_info['email']).first()
    if not user:  # if a user is not found, we'll create a new one
        user = get_or_create_user(user_info['email'], user_info['name'], "google", user_info['id'])

    # Create JWT token
    token = jwt.encode({
    'user_id': user.id,
    'exp': datetime.utcnow() + timedelta(hours=1),
    'nbf': datetime.utcnow()}, JWT_SECRET, algorithm='HS256')
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

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 403

        return f(current_user, *args, **kwargs)

    return decorator

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

def get_or_create_user(email, name=None, provider=None, provider_id=None):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name, provider=provider, provider_id=provider_id)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
     # handle/log exception
    return user


@socketio.on('connect', namespace='/training')
def connect():
    print("Client connected")
    emit('progress', {'progress': 'Connection established'})

@socketio.on('disconnect', namespace='/training')
def disconnect():
    print("Client disconnected")


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, ssl_context=(cert_path, key_path))
