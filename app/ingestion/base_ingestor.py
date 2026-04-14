from typing import List, Dict

from app.services.ingestion_service import IngestionService

from app.core.exceptions import ValidationError

class BaseIngestor:
    def __init__(self, ingestion_service: IngestionService, collection: str):
        self.ingestion_service = ingestion_service
        self.collection = collection

    async def ingest(
        self,
        ids: List[str],
        texts: List[str],
        metadata: List[Dict],
    ):
        self.logger.info(
            "Ingestion started",
            extra={"extra_data": {"collection": self.collection, "count": len(ids)}},
        )

        if not ids or not texts:
            self.logger.error(
                "Validation failed",
                extra={"extra_data": {"reason": "empty ids or texts"}},
            )
            raise ValidationError("IDs and texts must not be empty.")

        try:
            await self.ingestion_service.ingest_texts(
                collection=self.collection,
                ids=ids,
                texts=texts,
                metadata=metadata,
            )

            self.logger.info(
                "Ingestion successful",
                extra={"extra_data": {"collection": self.collection, "count": len(ids)}},
            )

        except Exception as e:
            self.logger.exception(
                "Ingestion failed",
                extra={"extra_data": {"collection": self.collection}},
            )
            raise