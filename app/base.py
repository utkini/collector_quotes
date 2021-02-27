import asyncio
from typing import List

from app.db.db_models import Exchanges, ExchangeTickers
from app.services import BitFinExClient, KuCoinClient, BinanceClient
from app.services.client_interface import ClientInterface
from app.services.data_models import ExchangeTickerModel


def get_exchange_client_by_name(exchange_name) -> ClientInterface:
    d = {
        'bitfinex': BitFinExClient,
        'kucoin': KuCoinClient,
        'binance': BinanceClient
    }
    return d.get(exchange_name)()


def collect_data():
    test_data = {
        'exchange': 'BitFinEx',
        'symbol': 'BTCUSD',
        'base': 'BTC',
        'quote': 'USD',
        'last_price': 50000.0,
        'time_received': 123
    }
    exchanges_name = [exchange.name for exchange in Exchanges.select()]
    # exchanges_name = ['bitfinex', 'kucoin', 'binance']
    clients = list()
    for exchange_name in exchanges_name:
        client = get_exchange_client_by_name(exchange_name)
        clients.append(client.get_updates())
    loop = asyncio.get_event_loop()
    result_tasks, _ = loop.run_until_complete(asyncio.wait(clients))
    for task in result_tasks:
        for quote in task.result():
            ExchangeTickers.create(**quote.as_dict())


if __name__ == '__main__':
    collect_data()
