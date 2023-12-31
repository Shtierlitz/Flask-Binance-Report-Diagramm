# project/app.py

from flask import Flask
from peewee import SqliteDatabase
from project.models import data_base
from project.views import report_bp, error_bp
from project.celery_maker import celery


def create_app():
    app = Flask(__name__, template_folder='project/templates', static_folder='project/static')

    app.config.from_pyfile("settings.py")
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.register_blueprint(report_bp)
    app.register_blueprint(error_bp)

    db_sq = SqliteDatabase(app.config['DATA_BASE'])
    data_base.initialize(db_sq)

    # clear all tasks
    celery.control.purge()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
