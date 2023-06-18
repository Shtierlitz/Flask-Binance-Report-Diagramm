# project/celery_maker.py
import json
import os

from celery import Celery
from datetime import timedelta
from project import tasks

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'params.json')
with open(file_path, 'r') as f:
    params = json.load(f)

celery.conf.beat_schedule = {
    'collect_data_from_binance': {
        'task': 'project.tasks.task_collect_data',
        'schedule': timedelta(seconds=int(params['update_interval'])),
        'args': (params['period'], params['num'], params['interval'])
    },
}
