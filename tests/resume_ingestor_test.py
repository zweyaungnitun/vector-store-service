
import pytest
from unittest.mock import AsyncMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ingestion.resume_ingestor import ResumeIngestor
from app.core.exceptions import ValidationError

@pytest.mark.asyncio
async def test_ingest_resume_success():
    mock_service = AsyncMock()
    resume_ingestor = ResumeIngestor(ingestion_service=mock_service)

    resume_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "experience": "5 years of software development",
        "years_experience": 5,
        "skills": ["Python", "Docker", "AWS"],
        "education": "BS Computer Science"
    }

    resume_id = await resume_ingestor.ingest_resume(resume_data)

    # Check that ingest_texts was called once
    mock_service.ingest_texts.assert_awaited_once()
    assert resume_id.startswith("resume_")

@pytest.mark.asyncio
async def test_ingest_resume_validation_error_missing_field():
    mock_service = AsyncMock()
    resume_ingestor = ResumeIngestor(ingestion_service=mock_service)

    invalid_resume_data = {
        "name": "Jane Doe",
        "experience": "3 years"
    }

    with pytest.raises(ValidationError) as exc_info:
        await resume_ingestor.ingest_resume(invalid_resume_data)
    
    assert "Missing required field: skills" in str(exc_info.value)
    mock_service.ingest_texts.assert_not_awaited()

@pytest.mark.asyncio
async def test_ingest_resume_validation_error_invalid_type():
    mock_service = AsyncMock()
    resume_ingestor = ResumeIngestor(ingestion_service=mock_service)

    invalid_resume_data = {
        "name": "Jane Doe",
        "experience": "3 years",
        "skills": "Python, Docker"
    }

    with pytest.raises(ValidationError) as exc_info:
        await resume_ingestor.ingest_resume(invalid_resume_data)
    
    assert "Skills must be a list" in str(exc_info.value)
    mock_service.ingest_texts.assert_not_awaited()
