import asyncio

from app.services.bitfinex.client import BitFinExClient

bfx = BitFinExClient()


async def run():
    print([t for t in await bfx.get_updates()])

t = asyncio.ensure_future(run())
asyncio.get_event_loop().run_until_complete(t)
