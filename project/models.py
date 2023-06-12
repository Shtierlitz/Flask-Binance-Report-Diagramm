# project/models.py

from peewee import *
import pandas as pd

data_base = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = data_base


class OriginReport(BaseModel):
    id = AutoField(null=False)
    symbol = CharField(max_length=10)
    date = DateTimeField()
    open_1 = DecimalField(max_digits=15, decimal_places=2)
    high = DecimalField(max_digits=15, decimal_places=2)
    low = DecimalField(max_digits=15, decimal_places=2)
    close = DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        table_name = 'binance_report'

    @classmethod
    def from_csv(cls, file_path: str, symbol: str):
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            cls.create(
                symbol=symbol,
                date=row['date'],
                open_1=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
            )
