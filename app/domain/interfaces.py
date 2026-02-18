
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VectorStore(ABC):

    @abstractmethod
    async def upsert(
        self,
        collection: str,
        ids: List[str],
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
    ) -> None:
        pass

    @abstractmethod
    async def search(
        self,
        collection: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def delete(
        self,
        collection: str,
        ids: List[str],
    ) -> None:
        pass
