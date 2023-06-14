# project/utils.py
import json
import os
import pandas as pd
import plotly.graph_objects as go


def create_pie_chart(dir_path):
    data_path = os.path.join(dir_path, 'data')
    symbols = ["BTCUSDT", "ETHUSDT", "AMBUSDT", "ADAUSDT", "DOGEUSDT", "ATOMUSDT", "ARBUSDT", "DOTUSDT", "ALPHAUSDT",
               "INJUSDT"]
    market_caps = []

    # Load parameters from file
    with open('params.json', 'r') as f:
        params = json.load(f)

    interval = params['interval']  # Get interval from params

    for symbol in symbols:
        file_path = os.path.join(data_path, f'{symbol}_{interval}.csv')
        df = pd.read_csv(file_path)
        market_cap = df['close'].iloc[-1]
        market_caps.append(market_cap)

    fig = go.Figure(data=[go.Pie(labels=symbols, values=market_caps)])
    return fig


def create_graph(file_path):
    df = pd.read_csv(file_path)

    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)

    return fig


def convert_interval_to_seconds(interval):
    """Converts update interval in seconds"""
    number = int(interval[:-1])
    unit = interval[-1].lower()
    params = ['h', 'd', 'm']
    if len(interval) > 2:
        raise ValueError("Update interval must be 2 letters only")

    if unit not in params:
        raise ValueError(
            f"Unknown symbols in update interval {interval}!\n"
            f"Must be like: 1h or 3d for example."
        )
    if unit == 'm':
        return number * 60
    elif unit == 'h':
        return number * 60 * 60
    elif unit == 'd':
        return number * 60 * 60 * 24


def create_interval_ending(interval):
    if interval[-1] == 'h':
        return 'hour/s'
    elif interval[-1] == 'd':
        return 'day/s'
    elif interval[-1] == 'M':
        return 'month/s'
