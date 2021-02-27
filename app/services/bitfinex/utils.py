from app.services.data_models import ExchangeTickerModel

exchange = 'BitFinEx'

'''
input data:
    // on trading pairs (ex. tBTCUSD)
  [
    SYMBOL,
    BID, 
    BID_SIZE, 
    ASK, 
    ASK_SIZE, 
    DAILY_CHANGE, 
    DAILY_CHANGE_RELATIVE, 
    LAST_PRICE, 
    VOLUME, 
    HIGH, 
    LOW
  ],
  // on funding currencies (ex. fUSD)
  [
    SYMBOL,
    FRR, 
    BID, 
    BID_PERIOD,
    BID_SIZE, 
    ASK, 
    ASK_PERIOD,
    ASK_SIZE,
    DAILY_CHANGE,
    DAILY_CHANGE_RELATIVE, 
    LAST_PRICE,
    VOLUME,
    HIGH, 
    LOW,
    _PLACEHOLDER,
    _PLACEHOLDER,
    FRR_AMOUNT_AVAILABLE
  ],
'''


def normalize_response(raw_ticker_data: list, ts) -> ExchangeTickerModel:
    if raw_ticker_data[0].startswith('t'):
        return ExchangeTickerModel(
            exchange=exchange,
            symbol=raw_ticker_data[0],  # BTCUSD
            base='I DONT KNOW',  # BTC
            quote=raw_ticker_data[2],  # USD
            last_price=raw_ticker_data[7],
            time_received=ts
        )
    elif raw_ticker_data[0].startswith('f'):
        return ExchangeTickerModel(
            exchange=exchange,
            symbol=raw_ticker_data[0],  # BTCUSD
            base='I DONT KNOW',  # BTC
            quote=raw_ticker_data[2],  # USD
            last_price=raw_ticker_data[10],
            time_received=ts
        )
