from peewee import *

from settings import db_params

psql_db = PostgresqlDatabase(**db_params)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = psql_db


class Exchanges(BaseModel):
    name = CharField(max_length=64, unique=True)


class ExchangeTickers(BaseModel):
    exchange = ForeignKeyField(Exchanges)
    symbol = CharField(max_length=64)
    base = CharField(max_length=64)
    quote = CharField(max_length=64)
    last_price = DoubleField()
    time_received = DateTimeField()
