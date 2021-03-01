from abc import ABC, abstractmethod
from typing import List

from services.data_models import ExchangeTickerModel


class ClientInterface(ABC):
    exchange: str

    @abstractmethod
    async def get_updates(self) -> List[ExchangeTickerModel]:
        """

        :return: ModelResponse
        """



