from app.services.data_models import ExchangeTickerModel

exchange = 'Binance'

'''
input data:
      {
    "symbol": "ETHBTC",
    "priceChange": "-0.00100400",
    "priceChangePercent": "-3.080",
    "weightedAvgPrice": "0.03218120",
    "prevClosePrice": "0.03259400",
    "lastPrice": "0.03159000",
    "lastQty": "0.21300000",
    "bidPrice": "0.03158800",
    "bidQty": "0.14200000",
    "askPrice": "0.03159300",
    "askQty": "3.84000000",
    "openPrice": "0.03259400",
    "highPrice": "0.03290400",
    "lowPrice": "0.03145700",
    "volume": "285680.85600000",
    "quoteVolume": "9193.55182698",
    "openTime": 1614206281723,
    "closeTime": 1614292681723,
    "firstId": 236081889,
    "lastId": 236442188,
    "count": 360300
  }
'''


def normalize_response(raw_ticker_data: dict, ts) -> ExchangeTickerModel:
    return ExchangeTickerModel(
        exchange=exchange,
        symbol=raw_ticker_data.get('symbol'),
        base='I DONT KNOW',
        quote=raw_ticker_data.get('quoteVolume'),
        last_price=raw_ticker_data.get('lastPrice'),
        time_received=ts
    )
