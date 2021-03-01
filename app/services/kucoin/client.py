import asyncio
import json
from datetime import datetime

import aiohttp as aiohttp
import requests

from logger import LOG
from services.client_interface import ClientInterface
from services.kucoin import urls
from services.data_models import ExchangeTickerModel


class KuCoinClient(ClientInterface):
    exchange = 'kucoin'

    def __init__(self, loop=None, *args, **kwargs):
        # self.loop = loop or asyncio.get_event_loop()
        self.tickers_base_quote = self._get_tickers_base_quote_matcher()

    def request(self, url: str):
        LOG.debug(url)
        response = requests.get(url)
        LOG.info(f'url: {url} status code: {response.status_code}')
        return response.json()

    def _get_tickers_base_quote_matcher(self):
        tickers_info = self.request(urls.symbols)
        tickers = tickers_info.get('data')
        ticker_base_quote = dict()
        for ticker in tickers:
            ticker_base_quote[ticker.get('symbol')] = (ticker.get('baseCurrency'), ticker.get('quoteCurrency'))
        return ticker_base_quote

    async def fetch(self, url):
        """
        Send a GET request to the kucoin api
        @return reponse
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            LOG.info(f'GET {url}')
            async with session.get(url) as resp:
                text = await resp.text()
                LOG.info(f'response - {text}')
                if resp.status != 200:
                    raise Exception(f'GET {url} failed with status {resp.status} - {text}')
                parsed = json.loads(text, parse_float=float)
                return parsed

    async def _get_info_tickers(self):
        tickers_info = await self.fetch(urls.all_tickers)
        LOG.info(f'Getting {len(tickers_info)} tickers')
        return tickers_info

    async def get_updates(self):
        LOG.info('start get update method')
        raw_tickers = await self._get_info_tickers()
        time = raw_tickers.get('data').get('time')
        dt = datetime.fromtimestamp(time / 1000)
        tickers = raw_tickers.get('data').get('ticker')
        res_list = list()
        for ticker in tickers:
            res_list.append(self._normalize_response(ticker, dt))
        return res_list

    def _normalize_response(self, data: dict, created_time) -> ExchangeTickerModel:
        symbol = data.get('symbol')
        return ExchangeTickerModel(
            exchange=self.exchange,
            symbol=symbol,
            base=self.tickers_base_quote[symbol][0],
            quote=self.tickers_base_quote[symbol][1],
            last_price=data.get('last'),
            time_received=created_time
        )


if __name__ == '__main__':
    ku_coin = KuCoinClient()
    print(ku_coin.get_updates())
