from typing import List, Dict, Any
from app.core.logger import get_logger
from app.services.vector_service import VectorService
from app.embeddings.base import EmbeddingProvider

logger = get_logger(__name__)


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
        batch_size: int = 100
    ) -> None:
        """
        Ingest texts in batches to handle memory limits and API rate limits.
        """
        if not (len(ids) == len(texts) == len(metadata)):
            raise ValueError("ids, texts and metadata length mismatch")

        total = len(ids)
        logger.info(f"Starting bulk ingestion into '{collection}': {total} records total.")
        
        for i in range(0, total, batch_size):
            end = min(i + batch_size, total)
            
            logger.info(f"Processing batch: {i} to {end} of {total} for collection '{collection}'")
            
            batch_ids = ids[i:end]
            batch_texts = texts[i:end]
            batch_metadata = metadata[i:end]
            
            # Embed the current batch
            vectors = await self.embedding_provider.embed(batch_texts)

            # Store the current batch
            await self.vector_service.store_vectors(
                collection=collection,
                ids=batch_ids,
                vectors=vectors,
                metadata=batch_metadata,
            )
        
        logger.info(f"Completed bulk ingestion into '{collection}': {total} records total.")