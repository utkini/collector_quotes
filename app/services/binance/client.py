import asyncio
import json
import time
import aiohttp as aiohttp
from app.logger import LOG
from app.services.binance import urls
from app.services.binance.utils import normalize_response
from app.services.client_interface import ClientInterface


class BinanceClient(ClientInterface):

    def __init__(self, loop=None, *args, **kwargs):
        self.loop = loop or asyncio.get_event_loop()

    async def fetch(self, url):
        """
        Send a GET request to the binance api
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
        tickers = await self._get_info_tickers()
        ts = time.time()
        res_list = list()
        for ticker in tickers:
            res_list.append(normalize_response(ticker, ts))
        return res_list


if __name__ == '__main__':
    binance = BinanceClient()
    print(binance.get_updates())
