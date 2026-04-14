from typing import Dict, Any, List
from uuid import uuid4

from app.ingestion.base_ingestor import BaseIngestor
from app.core.logger import get_logger
from app.core.exceptions import ValidationError


class KnowledgeIngestor(BaseIngestor):
    """
    Handles generic ingestion of unstructured text/documents into vector store.
    """

    def __init__(self, ingestion_service):
        super().__init__(
            ingestion_service=ingestion_service,
            collection="knowledge_data",
        )
        self.logger = get_logger(self.__class__.__name__)

    async def ingest_knowledge(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """
        Ingest a single piece of text.
        """
        if not text:
            raise ValidationError("Text content cannot be empty.")

        doc_id = f"know_{uuid4()}"
        
        meta = metadata or {}
        meta["type"] = "general_knowledge"
        
        await self.ingest(
            ids=[doc_id],
            texts=[text],
            metadata=[meta]
        )
        
        return doc_id

    async def ingest_bulk_knowledge(self, records: List[Dict[str, Any]], batch_size: int = 50) -> List[str]:
        """
        Ingest multiple knowledge records using streaming batches to manage memory.
        """
        if not records:
            raise ValidationError("Knowledge records list cannot be empty.")

        all_ids = []
        total = len(records)
        self.logger.info(f"Streaming ingestion started for {total} knowledge records.")

        for i in range(0, total, batch_size):
            chunk = records[i:i + batch_size]
            
            ids = []
            texts = []
            metadata = []

            for record in chunk:
                # Content processing
                text_content = record.get("text") or record.get("content")
                if not text_content:
                    text_content = self._build_text_from_flat_record(record)

                if not text_content or text_content.strip() == "":
                    continue

                doc_id = f"know_{uuid4()}"
                ids.append(doc_id)
                texts.append(text_content)
                
                # Metadata processing
                record_meta = record.get("metadata")
                if not isinstance(record_meta, dict):
                    meta = {k: v for k, v in record.items() if k not in ["text", "content"]}
                else:
                    meta = record_meta.copy()
                
                meta["type"] = "general_knowledge"
                metadata.append(meta)

            if ids:
                # Immediate ingestion of the current chunk
                await self.ingest(ids=ids, texts=texts, metadata=metadata)
                all_ids.extend(ids)
                self.logger.info(f"Ingested {len(all_ids)}/{total} records...")

        if not all_ids:
            raise ValidationError("No valid knowledge records found.")

        return all_ids

    def _build_text_from_flat_record(self, record: Dict[str, Any]) -> str:
        """
        Build a text representation for flat records that don't have a 'text' field.
        """
        parts = []
        for key, value in record.items():
            if value is not None and str(value).strip() != "":
                parts.append(f"{key}: {value}")
        return "\n".join(parts)
