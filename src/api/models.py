from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_oauthlib.client import OAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)
oauth = OAuth(app)
login_manager = LoginManager(app)

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    roles = db.Column(db.String(50))
    oauth_provider = db.Column(db.String(50))

# Initialize OAuth providers
google = oauth.remote_app(
    'google',
    consumer_key='YOUR_GOOGLE_OAUTH_CONSUMER_KEY',
    consumer_secret='YOUR_GOOGLE_OAUTH_CONSUMER_SECRET',
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

github = oauth.remote_app(
    'github',
    consumer_key='YOUR_GITHUB_OAUTH_CONSUMER_KEY',
    consumer_secret='YOUR_GITHUB_OAUTH_CONSUMER_SECRET',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

# Handle OAuth responses and user creation
def handle_oauth_response(provider, response, data_func):
    if response is None:
        return jsonify({"error": "Access denied"}), 403

    email = data_func(response)['email']

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(email=email, roles='user', oauth_provider=provider)
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=user.id, additional_claims={"roles": user.roles})
    return jsonify({"access_token": access_token}), 200

# Google OAuth endpoint
@app.route('/login/google', methods=['GET', 'POST'])
def login_google():
    if 'oauth_token' in request.args:
        resp = google.authorized_response()
        return handle_oauth_response('google', resp, lambda x: x['info']['email'])

    return google.authorize(callback=url_for('login_google', _external=True))

# GitHub OAuth endpoint
@app.route('/login/github', methods=['GET', 'POST'])
def login_github():
    if 'code' in request.args:
        resp = github.authorized_response()
        return handle_oauth_response('github', resp, lambda x: x['email'])

    return github.authorize(callback=url_for('login_github', _external=True))

# Traditional email/password login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id, additional_claims={"roles": user.roles})
    return jsonify({"access_token": access_token}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
