from dataclasses import dataclass


@dataclass
class ModelResponse:
    exchange: str
    symbol: str
    base: str  # ???
    quote: float
    last_price: float
    time_received: float
