from typing import List
from pinecone import Pinecone
from app.embeddings.base import EmbeddingProvider

class PineconeEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        api_key: str,
        model: str = "multilingual-e5-large",
    ):
        self.pc = Pinecone(api_key=api_key)
        self.model = model

    async def embed(self, texts: List[str]) -> List[List[float]]:
        # Pinecone Inference is synchronous in the current SDK, 
        # but we can wrap it if needed. However, since it's an API call, 
        # it's relatively fast for small batches.
        
        # multilingual-e5-large expects input_type="passage" or "query"
        # We'll use "passage" for ingestion by default.
        results = self.pc.inference.embed(
            model=self.model,
            inputs=texts,
            parameters={"input_type": "passage"}
        )
        
        return [item.values for item in results.data]

    async def health_check(self) -> bool:
        try:
            _ = self.pc.inference.embed(
                model=self.model,
                inputs=["health check"],
                parameters={"input_type": "query"}
            )
            return True
        except Exception:
            return False
