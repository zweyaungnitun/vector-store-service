import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VECTOR_DB_PROVIDER: str = os.getenv("VECTOR_DB_PROVIDER", "chroma")
    # Qdrant
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    # Chroma
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    CHROMA_COLLECTION: str = os.getenv("CHROMA_COLLECTION", "vectors")
    
    model_config = {
        "env_file": ".env"
    }

settings = Settings()
