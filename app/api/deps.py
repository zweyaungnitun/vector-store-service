from fastapi import Depends
from app.infrastructure.factory import get_vector_store
from app.services.vector_service import VectorService
from app.services.ingestion_service import IngestionService
from app.embeddings.factory import EmbeddingFactory
from app.ingestion.skill_ingestor import SkillIngestor
from app.ingestion.resume_ingestor import ResumeIngestor
from app.ingestion.job_ingestor import JobIngestor
from app.ingestion.excel_ingestor import ExcelIngestor
from app.ingestion.knowledge_ingestor import KnowledgeIngestor

from app.core.config import settings

def get_ingestion_service() -> IngestionService:
    # This is a simplified factory for dependencies
    vector_store = get_vector_store()
    vector_service = VectorService(vector_store)
    
    # Using configured embedding provider
    embedding_provider = EmbeddingFactory.create(
        provider=settings.EMBEDDING_PROVIDER,
        api_key=settings.OPENAI_API_KEY if settings.EMBEDDING_PROVIDER == "openai" else settings.PINECONE_API_KEY,
        model_name=settings.EMBEDDING_MODEL,
        dimensions=settings.EMBEDDING_DIMENSION
    )
    
    return IngestionService(
        embedding_provider=embedding_provider,
        vector_service=vector_service
    )

def get_skill_ingestor(
    ingestion_service: IngestionService = Depends(get_ingestion_service)
) -> SkillIngestor:
    return SkillIngestor(ingestion_service=ingestion_service)

def get_resume_ingestor(
    ingestion_service: IngestionService = Depends(get_ingestion_service)
) -> ResumeIngestor:
    return ResumeIngestor(ingestion_service=ingestion_service)

def get_job_ingestor(
    ingestion_service: IngestionService = Depends(get_ingestion_service)
) -> JobIngestor:
    return JobIngestor(ingestion_service=ingestion_service)

def get_excel_ingestor(
    ingestion_service: IngestionService = Depends(get_ingestion_service)
) -> ExcelIngestor:
    return ExcelIngestor(ingestion_service=ingestion_service)

def get_knowledge_ingestor(
    ingestion_service: IngestionService = Depends(get_ingestion_service)
) -> KnowledgeIngestor:
    return KnowledgeIngestor(ingestion_service=ingestion_service)
