from typing import Dict, Any, List
from uuid import uuid4

from app.ingestion.base_ingestor import BaseIngestor
from app.core.logger import get_logger
from app.core.exceptions import ValidationError


class JobIngestor(BaseIngestor):
    """
    Handles ingestion of job postings into vector store.
    """

    def __init__(self, ingestion_service):
        super().__init__(
            ingestion_service=ingestion_service,
            collection="jobs",
        )
        self.logger = get_logger(self.__class__.__name__)

    async def ingest_job(self, job_data: Dict[str, Any]) -> str:
        """
        Ingest a single job posting.

        Args:
            job_data: Dictionary containing job information

        Returns:
            job_id: Generated job ID
        """

        self.logger.info(
            "Job ingestion requested",
            extra={"extra_data": {"job_title": job_data.get("title")}},
        )

        try:
            self._validate(job_data)

            job_id = f"job_{uuid4()}"

            text_representation = self._build_text(job_data)

            metadata = {
                "type": "job",
                "title": job_data.get("title"),
                "company": job_data.get("company"),
                "location": job_data.get("location"),
            }

            await self.ingest(
                ids=[job_id],
                texts=[text_representation],
                metadata=[metadata],
            )

            self.logger.info(
                "Job ingestion successful",
                extra={
                    "extra_data": {
                        "job_id": job_id,
                        "company": job_data.get("company"),
                    }
                },
            )

            return job_id

        except ValidationError:
            self.logger.warning(
                "Job validation failed",
                extra={"extra_data": {"job_data": job_data}},
            )
            raise

        except Exception as e:
            self.logger.exception(
                "Unexpected error during job ingestion",
                extra={"extra_data": {"job_data": job_data}},
            )
            raise

    async def ingest_bulk_jobs(self, jobs: List[Dict[str, Any]]) -> List[str]:
        """
        Ingest multiple jobs at once.
        """
        if not jobs:
            raise ValidationError("Jobs list cannot be empty.")

        ids = []
        texts = []
        metadata = []

        for job in jobs:
            self._validate(job)
            job_id = f"job_{uuid4()}"
            ids.append(job_id)
            texts.append(self._build_text(job))
            metadata.append({
                "type": "job",
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
            })

        await self.ingest(ids=ids, texts=texts, metadata=metadata)
        self.logger.info("Bulk job ingestion completed", extra={"extra_data": {"count": len(ids)}})
        return ids

    def _validate(self, job_data: Dict[str, Any]) -> None:
        """
        Validate required job fields.
        """

        required_fields = ["title", "description", "company"]

        for field in required_fields:
            if not job_data.get(field):
                raise ValidationError(f"Missing required field: {field}")

    def _build_text(self, job_data: Dict[str, Any]) -> str:
        """
        Convert structured job data into searchable text.
        """

        parts: List[str] = [
            f"Job Title: {job_data.get('title')}",
            f"Company: {job_data.get('company')}",
            f"Location: {job_data.get('location', '')}",
            f"Description: {job_data.get('description')}",
            f"Skills: {', '.join(job_data.get('skills', []))}",
        ]

        return "\n".join(parts)