import asyncio
import json
import time
from datetime import datetime

import aiohttp as aiohttp
import requests

from logger import LOG
from services.binance import urls
from services.data_models import ExchangeTickerModel
from services.client_interface import ClientInterface


class BinanceClient(ClientInterface):
    exchange = 'binance'

    def __init__(self, loop=None, *args, **kwargs):
        # self.loop = loop or asyncio.get_event_loop()
        self.tickers_base_quote = self._get_tickers_base_quote_matcher()

    def request(self, url: str):
        LOG.debug(url)
        response = requests.get(url)
        LOG.info(f'url: {url} status code: {response.status_code}')
        return response.json()

    async def fetch(self, url):
        """
        Send a GET request to the binance api
        @return response
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

    def _get_tickers_base_quote_matcher(self):
        tickers_info = self.request(urls.symbols)
        tickers = tickers_info.get('symbols')
        ticker_base_quote = dict()
        for ticker in tickers:
            ticker_base_quote[ticker.get('symbol')] = (ticker.get('baseAsset'), ticker.get('quoteAsset'))
        return ticker_base_quote

    async def _get_info_tickers(self):
        tickers_info = await self.fetch(urls.all_tickers)
        LOG.info(f'Getting {len(tickers_info)} tickers')
        return tickers_info

    async def get_updates(self):
        LOG.info('Start get update method')
        tickers = await self._get_info_tickers()
        ts = time.time()
        dt = datetime.fromtimestamp(ts)
        res_list = list()
        for ticker in tickers:
            if self.tickers_base_quote.get(ticker.get('symbol')) is not None:
                ticker['base'] = self.tickers_base_quote[ticker.get('symbol')][0]
                ticker['quote'] = self.tickers_base_quote[ticker.get('symbol')][1]
                res_list.append(self._normalize_response(ticker, dt))
        return res_list

    def _normalize_response(self, raw_ticker_data: dict, created_time) -> ExchangeTickerModel:
        symbol = raw_ticker_data.get('symbol')
        return ExchangeTickerModel(
            exchange=self.exchange,
            symbol=symbol,
            base=self.tickers_base_quote[symbol][0],
            quote=self.tickers_base_quote[symbol][1],
            last_price=raw_ticker_data.get('lastPrice'),
            time_received=created_time
        )


if __name__ == '__main__':
    binance = BinanceClient()
    print(binance.get_updates())
