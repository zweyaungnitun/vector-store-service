from typing import Dict, Any, List
from uuid import uuid4

from app.ingestion.base_ingestor import BaseIngestor
from app.core.logger import get_logger
from app.core.exceptions import ValidationError


class ResumeIngestor(BaseIngestor):
    """
    Handles ingestion of resumes into vector store.
    """

    def __init__(self, ingestion_service):
        super().__init__(
            ingestion_service=ingestion_service,
            collection="resumes",
        )
        self.logger = get_logger(self.__class__.__name__)

    async def ingest_resume(self, resume_data: Dict[str, Any]) -> str:
        """
        Ingest a single resume.

        Args:
            resume_data: Dictionary containing resume information

        Returns:
            resume_id: Generated resume ID
        """

        self.logger.info(
            "Resume ingestion requested",
            extra={"extra_data": {"candidate_name": resume_data.get("name")}},
        )

        try:
            self._validate(resume_data)

            resume_id = f"resume_{uuid4()}"

            text_representation = self._build_text(resume_data)

            metadata = {
                "type": "resume",
                "name": resume_data.get("name"),
                "email": resume_data.get("email"),
                "years_experience": resume_data.get("years_experience"),
            }

            await self.ingest(
                ids=[resume_id],
                texts=[text_representation],
                metadata=[metadata],
            )

            self.logger.info(
                "Resume ingestion successful",
                extra={
                    "extra_data": {
                        "resume_id": resume_id,
                        "candidate_name": resume_data.get("name"),
                    }
                },
            )

            return resume_id

        except ValidationError:
            self.logger.warning(
                "Resume validation failed",
                extra={"extra_data": {"resume_data": resume_data}},
            )
            raise

        except Exception:
            self.logger.exception(
                "Unexpected error during resume ingestion",
                extra={"extra_data": {"resume_data": resume_data}},
            )
            raise

    def _validate(self, resume_data: Dict[str, Any]) -> None:
        """
        Validate required resume fields.
        """

        required_fields = ["name", "skills", "experience"]

        for field in required_fields:
            if not resume_data.get(field):
                raise ValidationError(f"Missing required field: {field}")

        if not isinstance(resume_data.get("skills"), list):
            raise ValidationError("Skills must be a list.")

    def _build_text(self, resume_data: Dict[str, Any]) -> str:
        """
        Convert structured resume data into searchable text.
        """

        parts: List[str] = [
            f"Candidate Name: {resume_data.get('name')}",
            f"Email: {resume_data.get('email', '')}",
            f"Experience: {resume_data.get('experience')}",
            f"Years of Experience: {resume_data.get('years_experience', '')}",
            f"Skills: {', '.join(resume_data.get('skills', []))}",
            f"Education: {resume_data.get('education', '')}",
        ]

        return "\n".join(parts)