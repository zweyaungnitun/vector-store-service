import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.vector_stores.chroma.store import ChromaStore
from app.services.vector_service import VectorService


async def main():
    
    store = ChromaStore(
        collection_name="test_collection",
        persist_directory="./chroma_test_db",
    )

    service = VectorService(store)

    dummy_vector = [0.1] * 1536

    await service.store_vectors(
        collection="test_collection",
        ids=["1"],
        vectors=[dummy_vector],
        metadata=[{"name": "Zwe", "type": "resume"}],
    )

    print("Inserted!")

    results = await service.search_vectors(
        collection="test_collection",
        query_vector=dummy_vector,
        top_k=1,
    )

    print("Search Results:")
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
