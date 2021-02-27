from abc import ABC, abstractmethod
from typing import List

from app.services.data_models import ExchangeTickerModel


class ClientInterface(ABC):

    @abstractmethod
    async def get_updates(self) -> List[ExchangeTickerModel]:
        """

        :return: ModelResponse
        """



