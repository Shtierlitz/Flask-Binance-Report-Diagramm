# project/tasks.py

from celery import shared_task
from project.get_and_create_data import collect_data, init_db


@shared_task
def task_collect_data(period, num, interval):
    init_db('binance.db')
    collect_data(period, num, interval)
