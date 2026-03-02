import pytest
import sys
import os
from app.embeddings.factory import EmbeddingFactory
from app.infrastructure.vector_stores.chroma.store import ChromaStore
from app.services.vector_service import VectorService
from app.services.ingestion_service import IngestionService


@pytest.mark.asyncio
async def test_ingestion_with_local_embeddings():

    collection_name = "test_collection_3321"
    persist_directory = "./chroma_test_db"

    embedding_provider = EmbeddingFactory.create(
        provider="local",
        model_name="all-MiniLM-L6-v2"
    )

    store = ChromaStore(
        collection_name=collection_name,
        persist_directory=persist_directory,
    )

    vector_service = VectorService(store)

    ingestion_service = IngestionService(
        embedding_provider=embedding_provider,
        vector_service=vector_service,
    )

    texts = [
        "Backend Engineer needed. Skills: Python, FastAPI, PostgreSQL."
    ]
    ids = ["job_001"]
    metadata = [{"role": "backend"}]

    await ingestion_service.ingest_texts(
        collection=collection_name,
        ids=ids,
        texts=texts,
        metadata=metadata,
    )

    query_vector = await embedding_provider.embed(
        ["Looking for Python API developer"]
    )

    results = await vector_service.search_vectors(
        collection=collection_name,
        query_vector=query_vector[0],
        top_k=1,
    )

    assert results is not None
    assert len(results) > 0