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

## Quick Start

Follow these steps to get the project up and running in minutes.

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd vector-store-service

# Create and activate a virtual environment
conda create -n vector-store python=3.11 -y
conda activate vector-store

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

The service requires a `.env` file for configuration. We provide a template to get you started:

```bash
cp .env.example .env
```

**Note:** By default, the project uses **ChromaDB** in persistent mode (saves to `./chroma_db`). No additional API keys are required for the default local setup.

### 3. Start the Backend Service

Launch the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

- **API URL**: `http://localhost:8000`
- **Health Check**: `http://localhost:8000/health`
- **Documentation**: `http://localhost:8000/docs`

### 4. Launch the Ingestion UI

The project features a premium drag-and-drop interface for managing your data.

1.  Navigate to the `frontend/` directory.
2.  Open `index.html` in your browser.
    - *Pro Tip*: For the best experience, serve it using a simple server:
      ```bash
      cd frontend
      python3 -m http.server 8080
      ```
    - Then visit `http://localhost:8080`.

### 5. Verify the Connection

- Ensure the "Target" dropdown is visible.
- The status bar should show "Ready" when files are selected.
- Successful ingestion will be reflected in the UI and the backend logs.


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
