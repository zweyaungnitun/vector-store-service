
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.main import app
from app.api.deps import get_skill_ingestor, get_resume_ingestor, get_job_ingestor

client = TestClient(app)

# Create mock objects
mock_skill_ingestor = AsyncMock()
mock_resume_ingestor = AsyncMock()
mock_job_ingestor = AsyncMock()

# Dependency overrides
@pytest.fixture(autouse=True)
def setup_overrides():
    app.dependency_overrides[get_skill_ingestor] = lambda: mock_skill_ingestor
    app.dependency_overrides[get_resume_ingestor] = lambda: mock_resume_ingestor
    app.dependency_overrides[get_job_ingestor] = lambda: mock_job_ingestor
    yield
    app.dependency_overrides = {}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_ingest_skill_api():
    mock_skill_ingestor.ingest_skill.return_value = "skill_123"
    
    skill_data = {
        "name": "Python",
        "category": "Programming",
        "level": "Advanced",
        "description": "Expert in Python"
    }

    response = client.post("/api/v1/ingest/skill", json=skill_data)
    
    assert response.status_code == 200
    assert response.json() == {"id": "skill_123", "status": "success"}
    mock_skill_ingestor.ingest_skill.assert_awaited_once()

@pytest.mark.asyncio
async def test_ingest_resume_api():
    mock_resume_ingestor.ingest_resume.return_value = "resume_456"

    resume_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "experience": "5 years",
        "years_experience": 5,
        "skills": ["Python", "AWS"],
        "education": "BS CS"
    }

    response = client.post("/api/v1/ingest/resume", json=resume_data)
    
    assert response.status_code == 200
    assert response.json() == {"id": "resume_456", "status": "success"}
    mock_resume_ingestor.ingest_resume.assert_awaited_once()

@pytest.mark.asyncio
async def test_ingest_job_api():
    mock_job_ingestor.ingest_job.return_value = "job_789"

    job_data = {
        "title": "Software Engineer",
        "description": "Looking for developers",
        "company": "Tech Inc",
        "location": "Remote",
        "skills": ["Python"]
    }

    response = client.post("/api/v1/ingest/job", json=job_data)
    
    assert response.status_code == 200
    assert response.json() == {"id": "job_789", "status": "success"}
    mock_job_ingestor.ingest_job.assert_awaited_once()
