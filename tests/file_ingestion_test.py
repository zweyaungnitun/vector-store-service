
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from io import BytesIO

from app.main import app
from app.api.deps import get_skill_ingestor, get_resume_ingestor, get_job_ingestor

client = TestClient(app)

# Mock objects
mock_skill_ingestor = AsyncMock()
mock_resume_ingestor = AsyncMock()
mock_job_ingestor = AsyncMock()

@pytest.fixture(autouse=True)
def setup_overrides():
    app.dependency_overrides[get_skill_ingestor] = lambda: mock_skill_ingestor
    app.dependency_overrides[get_resume_ingestor] = lambda: mock_resume_ingestor
    app.dependency_overrides[get_job_ingestor] = lambda: mock_job_ingestor
    yield
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_ingest_text_file_resume():
    mock_resume_ingestor.ingest_resume.return_value = "resume_txt_123"
    
    file_content = b"Candidate Name: Test User\nSkills: Python, Java"
    files = {"file": ("test_resume.txt", file_content, "text/plain")}
    
    response = client.post("/api/v1/ingest/file?target=resume", files=files)
    
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert "resume_txt_123" in response.json()["ids"]
    mock_resume_ingestor.ingest_resume.assert_awaited_once()

@pytest.mark.asyncio
async def test_ingest_csv_file_skills():
    mock_skill_ingestor.ingest_bulk_skills.return_value = ["skill_1", "skill_2"]
    
    # Simple CSV content
    csv_content = b"name,category,level\nPython,Language,Advanced\nFastAPI,Framework,Intermediate"
    files = {"file": ("skills.csv", csv_content, "text/csv")}
    
    response = client.post("/api/v1/ingest/file?target=skill", files=files)
    
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert len(response.json()["ids"]) == 2
    mock_skill_ingestor.ingest_bulk_skills.assert_awaited_once()
