
import pytest
from unittest.mock import AsyncMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ingestion.skill_ingestor import SkillIngestor
from app.core.exceptions import ValidationError
from typing import List, Dict

@pytest.mark.asyncio
async def test_ingest_skill_success():
    mock_service = AsyncMock()
    skill_ingestor = SkillIngestor(ingestion_service=mock_service)

    skill_data = {
        "name": "Python",
        "category": "Programming Language",
        "level": "Advanced",
        "description": "Python programming skills",
    }

    skill_id = await skill_ingestor.ingest_skill(skill_data)

    mock_service.ingest_texts.assert_awaited_once()
    assert skill_id.startswith("skill_")

@pytest.mark.asyncio
async def test_ingest_skill_validation_error():
    mock_service = AsyncMock()
    skill_ingestor = SkillIngestor(ingestion_service=mock_service)

    invalid_skill_data = {"category": "Programming Language"}

    with pytest.raises(ValidationError):
        await skill_ingestor.ingest_skill(invalid_skill_data)

    mock_service.ingest_texts.assert_not_awaited()

@pytest.mark.asyncio
async def test_ingest_bulk_skills_success():
    mock_service = AsyncMock()
    skill_ingestor = SkillIngestor(ingestion_service=mock_service)

    skills = [
        {"name": "Python", "category": "Programming", "level": "Advanced"},
        {"name": "SQL", "category": "Database", "level": "Intermediate"},
    ]

    skill_ids = await skill_ingestor.ingest_bulk_skills(skills)

    mock_service.ingest_texts.assert_awaited_once()
    assert len(skill_ids) == 2
    assert all(s.startswith("skill_") for s in skill_ids)

@pytest.mark.asyncio
async def test_ingest_bulk_skills_empty_list():
    mock_service = AsyncMock()
    skill_ingestor = SkillIngestor(ingestion_service=mock_service)

    with pytest.raises(ValidationError):
        await skill_ingestor.ingest_bulk_skills([])

    mock_service.ingest.assert_not_awaited()