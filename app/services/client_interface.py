from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable

from app.services.models import ModelResponse


class ClientInterface(ABC):

    @abstractmethod
    async def get_updates(self) -> ModelResponse:
        """

        :return: ModelResponse
        """



