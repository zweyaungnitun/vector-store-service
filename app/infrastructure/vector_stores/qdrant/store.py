from typing import List, Dict, Any
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
)
from app.domain.interfaces import VectorStore
from app.domain.models import VectorPoint, SearchResult


class QdrantStore(VectorStore):
    def __init__(
        self,
        url: str,
        api_key: str | None = None,
        vector_size: int = 1536,
        distance: Distance = Distance.COSINE,
    ):
        self.client = AsyncQdrantClient(
            url=url,
            api_key=api_key,
        )
        self.vector_size = vector_size
        self.distance = distance

    async def _ensure_collection(self, collection: str) -> None:
        collections = await self.client.get_collections()
        existing = [c.name for c in collections.collections]

        if collection not in existing:
            await self.client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=self.distance,
                ),
            )

    async def upsert(
        self,
        collection: str,
        points: List[VectorPoint],
    ) -> None:
        await self._ensure_collection(collection)

        qdrant_points = [
            PointStruct(
                id=point.id,
                vector=point.vector,
                payload=point.metadata,
            )
            for point in points
        ]

        await self.client.upsert(
            collection_name=collection,
            points=qdrant_points,
        )


    async def search(
        self,
        collection: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Filter | None = None,
    ) -> List[SearchResult]:

        results = await self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=top_k,
            query_filter=filters,
        )

        return [
            SearchResult(
                id=str(hit.id),
                score=hit.score,
                metadata=hit.payload or {},
            )
            for hit in results
        ]


    async def delete(
        self,
        collection: str,
        ids: List[str],
    ) -> None:
        await self.client.delete(
            collection_name=collection,
            points_selector=ids,
        )

