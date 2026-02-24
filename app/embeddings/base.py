from abc import ABC,abstractmethod
from typing import List

class EmbeddingProvider(ABC):
    """
    Base interface for embedding providers.
    """

    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Convert list of texts into list of embedding vectors.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if embedding provider is reachable.
        """
        pass