from dataclasses import dataclass, asdict


@dataclass
class ExchangeTickerModel:
    exchange: str
    symbol: str
    base: str
    quote: str
    last_price: float
    time_received: float

    def as_dict(self):
        return asdict(self)
