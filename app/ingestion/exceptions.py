class IngestionError(Exception):
    """Base ingestion error"""
    pass


class ValidationError(IngestionError):
    """Input validation failed"""
    pass


class EmbeddingError(IngestionError):
    """Embedding process failed"""
    pass


class VectorStoreError(IngestionError):
    """Vector storage failed"""
    pass