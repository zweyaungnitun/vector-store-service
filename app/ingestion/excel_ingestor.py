from typing import Dict, Any, List
from uuid import uuid4

from app.ingestion.base_ingestor import BaseIngestor
from app.core.logger import get_logger
from app.core.exceptions import ValidationError


class ExcelIngestor(BaseIngestor):
    """
    Handles generic ingestion of excel records into vector store.
    """

    def __init__(self, ingestion_service):
        super().__init__(
            ingestion_service=ingestion_service,
            collection="excel_data",
        )
        self.logger = get_logger(self.__class__.__name__)

    async def ingest_bulk_excel(
        self, 
        records: List[Dict[str, Any]], 
        id_column: str = None,
        text_columns: List[str] = None,
        batch_size: int = 50
    ) -> List[str]:
        """
        Ingest multiple excel records using streaming batches to manage memory.
        """
        if not records:
            raise ValidationError("Excel records list cannot be empty.")

        all_ids = []
        total = len(records)
        self.logger.info(f"Streaming Excel ingestion started for {total} records.")

        for i in range(0, total, batch_size):
            chunk = records[i:i + batch_size]
            
            ids = []
            texts = []
            metadata = []

            for record in chunk:
                # 1. Build text representation
                text = self._build_text(record, text_columns)
                
                # Skip records with no meaningful content
                if not text or text.strip() == "":
                    continue

                # 2. Determine ID
                if id_column and record.get(id_column):
                    record_id = str(record.get(id_column))
                else:
                    record_id = f"excel_{uuid4()}"
                
                ids.append(record_id)
                texts.append(text)
                
                # 3. Build metadata
                meta = {"type": "excel_record"}
                for k, v in record.items():
                    if v is None:
                        continue
                    
                    # Store values, cleaning will happen in the vector store layer
                    if isinstance(v, (str, int, float, bool)):
                        meta[k] = v
                    else:
                        meta[k] = str(v)
                        
                metadata.append(meta)

            if ids:
                # Immediate ingestion of the current chunk
                await self.ingest(ids=ids, texts=texts, metadata=metadata)
                all_ids.extend(ids)
                self.logger.info(f"Ingested {len(all_ids)}/{total} records...")

        if not all_ids:
            raise ValidationError("No valid records found in the excel data.")

        return all_ids

    def _build_text(self, record: Dict[str, Any], text_columns: List[str] = None) -> str:
        """
        Convert excel row into searchable embedding text.
        """
        parts = []
        
        if text_columns:
            # Only use specified columns for text
            for col in text_columns:
                val = record.get(col)
                if val is not None and str(val).strip() != "":
                    parts.append(f"{col}: {val}")
        else:
            # Default: use all columns
            for key, value in record.items():
                if value is not None and str(value).strip() != "":
                    parts.append(f"{key}: {value}")

        return "\n".join(parts)
