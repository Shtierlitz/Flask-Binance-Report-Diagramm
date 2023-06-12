# project/celery_maker.py

from celery import Celery
from datetime import timedelta

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.beat_schedule = {
        'collect_data_every_minute': {
            'task': 'project.tasks.task_collect_data',
            'schedule': timedelta(seconds=30),  # запуск каждую минуту
            # Здесь вы можете передать аргументы в вашу задачу, если они необходимы
            'args': ('hour', '1', '1h')  # замените на ваши аргументы
        },
    }


def init_celery(app):
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']


    celery.conf.update(app.config)

    celery.autodiscover_tasks(['project.tasks'], force=True)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
