from typing import List, Dict, Any
from app.domain.interfaces import VectorStore


class VectorService:

    def __init__(self, store: VectorStore):
        self.store = store

    async def store_vectors(
        self,
        collection: str,
        ids: List[str],
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
    ):
        await self.store.upsert(collection, ids, vectors, metadata)

    async def search_vectors(
        self,
        collection: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Dict[str, Any] | None = None,
    ):
        return await self.store.search(
            collection, query_vector, top_k, filters
        )

    async def delete_vectors(
        self,
        collection: str,
        ids: List[str],
    ):
        await self.store.delete(collection, ids)
