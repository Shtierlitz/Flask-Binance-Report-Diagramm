# project/tasks.py
import os

from celery import shared_task
from project.get_and_create_data import collect_data, init_db


@shared_task
def task_collect_data(period, num, interval):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    init_db(f'{base_dir}/binance.db')
    collect_data(period, num, interval)
