from app.domain.interfaces import VectorStore
from app.core.config import settings

from app.infrastructure.vector_stores.qdrant.store import QdrantStore
from app.infrastructure.vector_stores.chroma.store import ChromaStore


def get_vector_store() -> VectorStore:

    provider = settings.VECTOR_DB_PROVIDER.lower()

    if provider == "qdrant":
        return QdrantStore(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

    elif provider == "chroma":
        return ChromaStore(
            collection_name=settings.CHROMA_COLLECTION,
            persist_directory=settings.CHROMA_PERSIST_DIR,
        )

    else:
        raise ValueError(f"Unsupported vector DB provider: {provider}")
