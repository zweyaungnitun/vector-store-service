from typing import List, Dict, Any
from app.services.vector_service import VectorService
from app.embeddings.base import EmbeddingProvider


class IngestionService:

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_service: VectorService,
    ):
        self.embedding_provider = embedding_provider
        self.vector_service = vector_service

    async def ingest_texts(
        self,
        collection: str,
        ids: List[str],
        texts: List[str],
        metadata: List[Dict[str, Any]],
    ) -> None:

        if not (len(ids) == len(texts) == len(metadata)):
            raise ValueError("ids, texts and metadata length mismatch")

        vectors = await self.embedding_provider.embed(texts)

        await self.vector_service.store_vectors(
            collection=collection,
            ids=ids,
            vectors=vectors,
            metadata=metadata,
        )