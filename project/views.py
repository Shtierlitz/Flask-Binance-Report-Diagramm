# project/views.py
import os

from flask import render_template, Blueprint, abort
import plotly
import json

from .utils import create_graph, create_pie_chart, create_interval_ending

report_bp = Blueprint('diagrams', __name__)
error_bp = Blueprint('errors', __name__)


@report_bp.route('/<string:file_name>/')
def candlestick_diagram(file_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', f'{file_name}.csv')
    if not os.path.exists(file_path):
        abort(404)
    fig = create_graph(file_path)
    with open('params.json', 'r') as f:
        params = json.load(f)
    interval_start = file_name[-2]
    interval_end = create_interval_ending(file_name)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    context = {
        'period': params['period'],
        'num': params['num'],
        'interval_end': interval_end,
        'interval_start': interval_start,
        'graphJSON': graph_json
    }

    return render_template('candlestick.html', title="Diagram", context=context, interval=file_name[:-3])


@report_bp.route('/market_caps/')
def market_caps_diagram():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fig = create_pie_chart(base_dir)
    with open('params.json', 'r') as f:
        params = json.load(f)
    interval_start = params['interval'][0]
    interval_end = create_interval_ending(params['interval'])
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    context = {
        'period': params['period'],
        'num': params['num'],
        'interval_end': interval_end,
        'interval_start': interval_start,
        'graphJSON': graph_json
    }
    return render_template('pie_chart.html', title="Market Caps", context=context)


@report_bp.route('/')
def start_page():
    return render_template('index.html', title="Binance report")


@error_bp.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404
