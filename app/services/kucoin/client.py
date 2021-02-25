import asyncio
import json

import aiohttp as aiohttp
import urls
from app.logger import LOG
from app.services.client_interface import ClientInterface
from app.services.kucoin.utils import normalize_response


class KuCoinClient(ClientInterface):

    def __init__(self, loop=None, *args, **kwargs):
        self.loop = loop or asyncio.get_event_loop()

    async def fetch(self, url):
        """
        Send a GET request to the kucoin api
        @return reponse
        """
        async with aiohttp.ClientSession() as session:
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
        tickers = tickers.get('ticker')
        res_list = list()
        for ticker in tickers:
            res_list.append(normalize_response(ticker))
        return res_list


if __name__ == '__main__':
    ku_coin = KuCoinClient()
    print(ku_coin.get_updates())
