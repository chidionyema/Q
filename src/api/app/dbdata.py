from app import db
from datetime import datetime
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
    is_active = db.Column(db.Boolean, default=False) 
    

    def __repr__(self):
            return f"<User {self.email}>"    


class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, token, user_id, expiration_time):
        self.token = token
        self.user_id = user_id
        self.expiration_time = expiration_time

class TaskResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    task_id = db.Column(db.String, unique=True, nullable=False)
    result = db.Column(db.JSON, nullable=False)