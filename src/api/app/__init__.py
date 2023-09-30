# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery, Task
from flask_socketio import SocketIO
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)
    return app

app = create_app()  # Flask app

socketio = SocketIO(message_queue='redis://localhost:6379/0', cors_allowed_origins="*")

class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super(ContextTask, self).__call__(*args, **kwargs)

celery = Celery(app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.update(app.config)
celery.Task = ContextTask  # Setting the default Task class to ContextTask
