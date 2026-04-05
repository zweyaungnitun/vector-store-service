# Vector Store Service

A FastAPI-based service for ingesting and searching HR-related data (Skills, Resumes, Jobs) using vector embeddings and vector databases (Chroma or Qdrant).

## Features

- **Multi-format Ingestion**: Supports PDF, CSV, Excel, and Plain Text files.
- **Bulk Ingestion**: Efficiently ingest multiple records at once via JSON.
- **Vector Search**: Semantic search capabilities for matching skills, resumes, and jobs.
- **Flexible Providers**: Supports Chroma (local) and Qdrant (cloud/local) as vector stores.
- **Embedding Support**: Supports both OpenAI and local Sentence-Transformers.

## Prerequisites

- Python 3.10 or 3.11
- Conda (recommended) or virtualenv

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd vector-store-service
   ```

2. **Create and activate a virtual environment**:
   ```bash
   conda create -n vector-store python=3.11
   conda activate vector-store
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**:
   Copy the example environment file and update it with your settings:
   ```bash
   cp .env.example .env
   ```

## Running the Project

To start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The service will be available at `http://localhost:8000`.

## Using the Ingestion UI

A premium drag-and-drop UI is available in the `frontend/` directory.

1. **Start the Backend**: Ensure the FastAPI server is running (`uvicorn app.main:app --reload`).
2. **Open the UI**: Simply open `frontend/index.html` in any modern web browser.
3. **Upload**: Select your target type (Resume, Job, or Skill), drop your files, and click "Ingest Data".

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Running Tests

To run the full test suite:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/skill_ingestor_test.py
```

## Folder Structure

- `app/api/`: API routes, schemas, and dependencies.
- `app/core/`: Configuration, logger, and common exceptions.
- `app/embeddings/`: Embedding providers (OpenAI, Local).
- `app/infrastructure/`: Vector store implementations (Chroma, Qdrant).
- `app/ingestion/`: Ingestors for Skills, Resumes, and Jobs.
- `app/services/`: Business logic services.
- `app/utils/`: File processing and other utilities.
- `tests/`: Comprehensive test suite.
