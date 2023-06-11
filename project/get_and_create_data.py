# project/get_and_create_data.py

import os
import pandas as pd
from binance.client import Client
import argparse

# Устанавливаем API и секретный ключ
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("SECRET_KEY")

# Создаем клиент Binance
client = Client(api_key, api_secret)


def get_binance_bars(symbol, interval, start_date, end_date):
    bars = client.get_historical_klines(symbol, interval, start_date, end_date)
    for line in bars:
        del line[5:]  # Мы не используем эти данные, поэтому удаляем их

    return bars


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--period', dest="period", help="Input day or week or year ago")
    parser.add_argument('--num', dest="num", help="Input number of day or week or year ago")
    parser.add_argument('--interval', dest="interval", help="Input interval of report. Example: 1d, 4h, 1h")
    args = parser.parse_args()
    # Получаем данные за выбранный период
    start_date = f"{args.num} {args.period} ago UTC"
    end_date = "now UTC"

    # Котировки, которые нам нужны
    symbols = ["BTCUSDT", "ETHUSDT"]
    interval = args.interval
    if args.period and args.num and args.interval:
        for symbol in symbols:
            bars = get_binance_bars(symbol, interval, start_date, end_date)

            # Преобразуем в DataFrame
            df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])

            # Конвертируем timestamp в datetime
            df['date'] = pd.to_datetime(df['date'], unit='ms')

            # Сохраняем CSV файл в папку data
            df.to_csv(f'data/{symbol}_{interval}.csv', index=False)
    else:
        print(
            'You must input arguments properly. Example: python get_and_create_data.py --period "week" --num "1" --interval "4h"'
        )
