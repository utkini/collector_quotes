from app.db.db_models import *

from app.services import supported_exchanges

# init psql tables
psql_db.connect()
psql_db.create_tables([Exchanges, ExchangeTickers])

# create supported exchanges
for exchange_name in supported_exchanges:
    Exchanges.get_or_create(name=exchange_name)
