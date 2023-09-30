# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery, Task
from flask_socketio import SocketIO
from flask_mail import Mail
import logging
import re

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)
    return app

app = create_app()  # Flask app

# Custom logger for Flask-SocketIO
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('socketio')
log.setLevel(logging.INFO)

# Custom Log Handler to censor session IDs
class CustomLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        # Censoring session IDs from logs (example pattern)
        msg = re.sub(r"'sid': '\w+'", "'sid': 'CENSORED'", msg)
        print(msg)

handler = CustomLogHandler()
log.addHandler(handler)

socketio = SocketIO(app, message_queue='redis://localhost:6379/0', cors_allowed_origins="*")

class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super(ContextTask, self).__call__(*args, **kwargs)

celery = Celery(app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.update(app.config)
celery.Task = ContextTask  # Setting the default Task class to ContextTask
