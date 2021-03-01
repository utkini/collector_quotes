from time import sleep
from peewee import *
from db.db_models import Exchanges, ExchangeTickers
from logger import LOG

from services import supported_exchanges
from settings import db_params

try:
    LOG.info('Creating tables')

    psql_db = PostgresqlDatabase(**db_params)
    sleep(10)
    psql_db.connect()
    test = psql_db.create_tables([Exchanges, ExchangeTickers])

    LOG.info('Tables created')

    # create supported exchanges
    for exchange_name in supported_exchanges:
        exchange = Exchanges.get_or_create(name=exchange_name)
        LOG.info(exchange)
except Exception as e:
    LOG.warning(e)
