# project/utils.py
import os

import pandas as pd
import plotly.graph_objects as go

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'data', 'BTCUSDT_4h.csv')

df = pd.read_csv(file_path)

fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.update_layout(xaxis_rangeslider_visible=False)
