# project/views.py

from flask import render_template, request, Blueprint, abort
import plotly
import json

from .utils import fig

report_bp = Blueprint('drivers', __name__)
error_bp = Blueprint('errors', __name__)


@report_bp.route('/')
def start_page():


    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', title="Binance report", graphJSON=graph_json)


@error_bp.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404
