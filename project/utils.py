# project/utils.py
import os
import pandas as pd
import plotly.graph_objects as go

def create_graph(file_path):
    df = pd.read_csv(file_path)

    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)

    return fig
