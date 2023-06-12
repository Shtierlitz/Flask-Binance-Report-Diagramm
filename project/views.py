# project/views.py
import os

from flask import render_template, request, Blueprint, abort
import plotly
import json

from .utils import create_graph

report_bp = Blueprint('diagrams', __name__)
error_bp = Blueprint('errors', __name__)



@report_bp.route('/btc_usdt/<string:file_name>/')
def candlestick_diagram(file_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', f'{file_name}.csv')
    if not os.path.exists(file_path):
        abort(404)
    fig = create_graph(file_path)

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('candlestick.html', title="Diagram", graphJSON=graph_json)


@report_bp.route('/')
def start_page():
    return render_template('index.html', title="Binance report")

@error_bp.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404
