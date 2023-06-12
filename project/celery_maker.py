from celery import Celery

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

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
