from typing import Dict, Any, List
from uuid import uuid4

from app.ingestion.base_ingestor import BaseIngestor
from app.core.logger import get_logger
from app.core.exceptions import ValidationError
from typing import List, Dict

class SkillIngestor(BaseIngestor):
    """
    Handles ingestion of skills into vector store.
    Useful for skill normalization and semantic matching.
    """

    def __init__(self, ingestion_service):
        super().__init__(
            ingestion_service=ingestion_service,
            collection="skills",
        )
        self.logger = get_logger(self.__class__.__name__)

    async def ingest_skill(self, skill_data: Dict[str, Any]) -> str:
        """
        Ingest a single skill.
        """

        self.logger.info(
            "Skill ingestion requested",
            extra={"extra_data": {"skill_name": skill_data.get("name")}},
        )

        try:
            self._validate(skill_data)

            skill_id = f"skill_{uuid4()}"

            text_representation = self._build_text(skill_data)

            metadata = {
                "type": "skill",
                "name": skill_data.get("name"),
                "category": skill_data.get("category"),
                "level": skill_data.get("level"),
            }

            await self.ingest(
                ids=[skill_id],
                texts=[text_representation],
                metadata=[metadata],
            )

            self.logger.info(
                "Skill ingestion successful",
                extra={
                    "extra_data": {
                        "skill_id": skill_id,
                        "skill_name": skill_data.get("name"),
                    }
                },
            )

            return skill_id

        except ValidationError:
            self.logger.warning(
                "Skill validation failed",
                extra={"extra_data": {"skill_data": skill_data}},
            )
            raise

        except Exception:
            self.logger.exception(
                "Unexpected error during skill ingestion",
                extra={"extra_data": {"skill_data": skill_data}},
            )
            raise

    async def ingest_bulk_skills(self, skills: List[Dict[str, Any]]) -> List[str]:
        """
        Ingest multiple skills at once (more efficient).
        """

        if not skills:
            raise ValidationError("Skills list cannot be empty.")

        ids = []
        texts = []
        metadata = []

        for skill in skills:
            self._validate(skill)

            skill_id = f"skill_{uuid4()}"
            ids.append(skill_id)

            texts.append(self._build_text(skill))

            metadata.append(
                {
                    "type": "skill",
                    "name": skill.get("name"),
                    "category": skill.get("category"),
                    "level": skill.get("level"),
                }
            )

        await self.ingest(ids=ids, texts=texts, metadata=metadata)

        self.logger.info(
            "Bulk skill ingestion completed",
            extra={"extra_data": {"count": len(ids)}},
        )

        return ids

    def _validate(self, skill_data: Dict[str, Any]) -> None:
        """
        Validate skill fields.
        """

        if not skill_data.get("name"):
            raise ValidationError("Skill name is required.")

        if not isinstance(skill_data.get("name"), str):
            raise ValidationError("Skill name must be a string.")

    def _build_text(self, skill_data: Dict[str, Any]) -> str:
        """
        Convert skill into searchable embedding text.
        """

        parts = [
            f"Skill Name: {skill_data.get('name')}",
            f"Category: {skill_data.get('category', '')}",
            f"Level: {skill_data.get('level', '')}",
            f"Description: {skill_data.get('description', '')}",
        ]

        return "\n".join(parts)