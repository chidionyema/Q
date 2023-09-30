import os
from celery import Celery

BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


celery = Celery('tasks', broker=CELERY_RESULT_BACKEND, backend=CELERY_RESULT_BACKEND)
