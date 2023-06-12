# project/settings.py

import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True
FOLDER_PATH = '../project/static/data'
# BASE_DIR = os.path.dirname(os.path.abspath("app.py"))
# DATA_DIR = os.path.join(BASE_DIR, 'static', 'data')
DATA_BASE = "binance.db"

# celery
REDIS_PORT = '6379'
REDIS_HOST = 'localhost'
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_TASK_LIST = ['project.tasks']
