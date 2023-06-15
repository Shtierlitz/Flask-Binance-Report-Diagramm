# project/tasks.py
import os

from celery import shared_task
from get_and_create_data import collect_data, init_db


@shared_task
def task_collect_data(period, num, interval):
    init_db('binance.db')
    collect_data(period, num, interval)
