import os

from peewee import *

params = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_USER'),
    'host': os.environ.get('POSTGRES_HOST')
}

psql_db = PostgresqlDatabase(**params)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = psql_db


class Exchanges(BaseModel):
    name = CharField(max_length=64, unique=True)


class ExchangeTickers(BaseModel):
    exchange = ForeignKeyField(Exchanges),
    symbol = CharField(max_length=64),
    base = CharField(max_length=64),
    quote = CharField(max_length=64),
    last_price = DoubleField(),
    time_received = DateTimeField()
