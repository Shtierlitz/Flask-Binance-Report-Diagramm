import os
import pandas as pd
from binance.client import Client
import argparse
from peewee import SqliteDatabase
import json  # Add this import

try:
    from project.models import OriginReport, data_base
    from project.utils import convert_interval_to_seconds
except ModuleNotFoundError:
    from models import OriginReport, data_base
    from utils import convert_interval_to_seconds

# API и секретный ключ
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("SECRET_KEY")

# клиент Binance
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

    symbols = ["BTCUSDT", "ETHUSDT", "AMBUSDT", "ADAUSDT", "DOGEUSDT", "ATOMUSDT", "ARBUSDT", "DOTUSDT", "ALPHAUSDT",
               "INJUSDT"]

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
    parser.add_argument('--update_interval', dest="update_interval",
                        help="Input interval for data updating. Example: 1d, 4h, 1w")
    args = parser.parse_args()

    if args.period and args.num and args.interval and args.update_interval:
        collect_data(args.period, args.num, args.interval)

        update_interval = convert_interval_to_seconds(args.update_interval)
        # Save parameters to params.json
        with open('params.json', 'w') as f:
            json.dump({
                'period': args.period,
                'num': args.num,
                'interval': args.interval,
                'update_interval': update_interval
            }, f)
    else:
        print(
            'You must input arguments properly. Example: '
            'python get_and_create_data.py --period "week" --num "1" --interval "4h" --update_interval "1h"'
        )
