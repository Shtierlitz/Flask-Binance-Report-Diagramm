# project/get_and_create_data.py

import os
import pandas as pd
from binance.client import Client
import argparse
from peewee import SqliteDatabase
try:
    from project.models import OriginReport, data_base
except ModuleNotFoundError:
    from models import OriginReport, data_base

# Устанавливаем API и секретный ключ
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("SECRET_KEY")

# Создаем клиент Binance
client = Client(api_key, api_secret)


def init_db(db_path):
    db_sq = SqliteDatabase(db_path)
    data_base.initialize(db_sq)
    data_base.create_tables([OriginReport], safe=True)

def get_binance_bars(symbol, interval, start_date, end_date):
    bars = client.get_historical_klines(symbol, interval, start_date, end_date)
    for line in bars:
        del line[5:]  # Мы не используем эти данные, поэтому удаляем их

    return bars


def read_data_from_csv_and_save_to_db(symbol: str, interval: str, dir_path=None):
    file_path = os.path.join(dir_path, 'data', f'{symbol}_{interval}.csv')
    OriginReport.from_csv(file_path, symbol)

def collect_data(period, num, interval):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path, 'data')
    start_date = f"{num} {period} ago UTC"
    end_date = "now UTC"

    symbols = ["BTCUSDT", "ETHUSDT"]

    for symbol in symbols:
        bars = get_binance_bars(symbol, interval, start_date, end_date)

        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])

        df['date'] = pd.to_datetime(df['date'], unit='ms')

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        df.to_csv(os.path.join(data_path, f'{symbol}_{interval}.csv'), index=False)

        read_data_from_csv_and_save_to_db(symbol, interval, dir_path)


if __name__ == "__main__":
    init_db('binance.db')
    parser = argparse.ArgumentParser()
    parser.add_argument('--period', dest="period", help="Input day or week or year ago")
    parser.add_argument('--num', dest="num", help="Input number of day or week or year ago")
    parser.add_argument('--interval', dest="interval", help="Input interval of report. Example: 1d, 4h, 1h")
    args = parser.parse_args()

    if args.period and args.num and args.interval:
        collect_data(args.period, args.num, args.interval)
    else:
        print(
            'You must input arguments properly. Example: python get_and_create_data.py --period "week" --num "1" --interval "4h"'
        )
