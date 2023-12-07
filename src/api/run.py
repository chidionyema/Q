# from gevent import monkey
# monkey.patch_all()

import json
import eventlet
eventlet.monkey_patch(socket=True, select=True)

import logging
import os

# Third-party libraries
from flask import  jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_migrate import Migrate
from auth import auth_blueprint
from flask_socketio import  emit 
from dotenv import load_dotenv
from app import socketio, db
from app.dbdata import  ModelCategory, MLModel, EnsembleStrategy, ModelOptimizer

load_dotenv()

# Access environment variables
secret_key = os.environ.get('SECRET_KEY')
database_uri = os.environ.get('DATABASE_URI')
base_uri = os.environ.get('BASE_URI')
sql_alchemy_track_modifications = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
flask_app = os.environ.get('FLASK_APP')
flask_env = os.environ.get('FLASK_ENV')

from app import app
#app = create_app()
app.debug = True
app.logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
app.logger.addHandler(handler)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
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
migrate = Migrate(app, db) 

@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return None
# Import caching extension and initialize it
from flask_caching import Cache
cache = Cache(app)

# Caching configuration (adjust cache_timeout as needed)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  # Cache for 1 hour


@app.route('/fetch_model_categories', methods=['GET'])
@cache.cached()  # Cache the response
def fetch_model_categories():
    # Query all rows from the model_categories table
    categories = ModelCategory.query.all()

    if categories:
        # Convert the queried categories to a list of dictionaries
        data = [{
            'id': category.id,
            'category': category.category,
            'code': category.code
        } for category in categories]
        
        return jsonify(data)
    else:
        return jsonify({'error': 'No model categories found in the database'}), 404


@app.route('/fetch-models', methods=['GET'])
@cache.cached()  # Cache the response
def fetch_models():
    # Query all rows from ml_models table
    models = MLModel.query.all()

    if models:
        # Convert the queried models to a list of dictionaries
        data = [{
            'id': model.id,
            'name': model.name,
            'description': model.description,
            'category_id': model.category_id,
            'code': model.code
        } for model in models]
        
        return jsonify(data)
    else:
        return jsonify({'error': 'No models found in the database'}), 404

@app.route('/fetch_ensembles', methods=['GET'])
@cache.cached()  # Cache the response
def fetch_ensembles():
    # Query all rows from ensembles table
    ensembles = EnsembleStrategy.query.all()

    if ensembles:
        # Convert the queried ensembles to a list of dictionaries
        data = [{
            'id': ensemble.id,
            'name': ensemble.name,
            'description': ensemble.description,
            'code': ensemble.code
            # Convert other attributes as needed
        } for ensemble in ensembles]
        
        return jsonify(data)
    else:
        return jsonify({'error': 'No ensembles found in the database'}), 404

@app.route('/fetch_optimizers', methods=['GET'])
@cache.cached()  # Cache the response
def fetch_optimizers():
    # Query all rows from the optimizers table
    optimizers = ModelOptimizer.query.all()

    if optimizers:
        # Convert the queried optimizers to a list of dictionaries
        data = [{
            'id': optimizer.id,
            'name': optimizer.name,
            'description': optimizer.description,
            'code': optimizer.code
            # ... add other attributes as needed
        } for optimizer in optimizers]
        
        return jsonify(data)
    else:
        return jsonify({'error': 'No optimizers found in the database'}), 404


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

from app.tasks import train_model_task  # Import your task

# Rest of your Celery configuration

@socketio.on('submit_configurations')
def handle_train_model_event(data):
    try:
        logging.info(f'Received train_model event with data: {data}')

        # Initialize an empty collection for configurations
        configurations = []

        # Process each stock configuration and add to the collection
        for item in data:
            symbol = item['symbol']
            config = item['config']

            start_date = config.get('startDate')
            end_date = config.get('endDate')
            model_name = config.get('Model')
            optimizer_name = config.get('Optimizer')
            voting_strategy_name = config.get('Voting Strategy')

            # Build the configuration dictionary for each stock
            stock_config = {
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date,
                'model_name': model_name,
                'optimizer_name': optimizer_name,
                'voting_strategy_name': voting_strategy_name
            }
            configurations.append(stock_config)

            logging.info(f'Added to configurations: {stock_config}')

        # Trigger the training task with the collection of configurations
        train_model_task.delay(configurations)

        # Emit a message to the client
        emit('training_started', {'message': 'Training has started'})

    except Exception as e:
        # Handle exceptions gracefully and log errors
        logging.error(f'Error processing configurations: {str(e)}')
        emit('training_error', {'error_message': str(e)})

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
