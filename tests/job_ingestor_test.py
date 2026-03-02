
import pytest
from unittest.mock import AsyncMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ingestion.job_ingestor import JobIngestor
from app.core.exceptions import ValidationError

@pytest.mark.asyncio
async def test_ingest_job_success():
    mock_service = AsyncMock()
    job_ingestor = JobIngestor(ingestion_service=mock_service)

    job_data = {
        "title": "Senior Software Engineer",
        "description": "We are looking for a Python expert.",
        "company": "Tech Corp",
        "location": "Remote",
        "skills": ["Python", "FastAPI"]
    }

    job_id = await job_ingestor.ingest_job(job_data)
    mock_service.ingest_texts.assert_awaited_once()
    assert job_id.startswith("job_")

@pytest.mark.asyncio
async def test_ingest_job_validation_error():
    mock_service = AsyncMock()
    job_ingestor = JobIngestor(ingestion_service=mock_service)

    invalid_job_data = {
        "title": "Senior Software Engineer",
        "description": "Python expert"
    }

    with pytest.raises(ValidationError) as exc_info:
        await job_ingestor.ingest_job(invalid_job_data)
    
    assert "Missing required field: company" in str(exc_info.value)
    mock_service.ingest_texts.assert_not_awaited()
