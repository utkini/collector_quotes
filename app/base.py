import asyncio

from db.db_models import Exchanges, ExchangeTickers
from logger import LOG
from services import BitFinExClient, KuCoinClient, BinanceClient
from services.client_interface import ClientInterface


def get_exchange_client_by_name(exchange_name) -> ClientInterface:
    d = {
        'bitfinex': BitFinExClient,
        'kucoin': KuCoinClient,
        'binance': BinanceClient
    }
    return d.get(exchange_name)()


def collect_data():
    exchanges_name = [exchange.name for exchange in Exchanges.select()]
    clients = list()
    for exchange_name in exchanges_name:
        client = get_exchange_client_by_name(exchange_name)
        clients.append(client.get_updates())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result_tasks, _ = loop.run_until_complete(asyncio.wait(clients))
    for task in result_tasks:
        exchange_name = task.result()[0].exchange
        exchange = Exchanges.get(name=exchange_name)
        LOG.info(f'{exchange} with {exchange_name}')
        for quote in task.result():
            ExchangeTickers.create(
                exchange=exchange,
                symbol=quote.symbol,
                base=quote.base,
                quote=quote.quote,
                last_price=quote.last_price,
                time_received=quote.time_received
            )
        LOG.info(f'tickers from {exchange_name} added')


if __name__ == '__main__':
    collect_data()
