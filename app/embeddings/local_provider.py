
from typing import List
from app.embeddings.base import EmbeddingProvider
from sentence_transformers import SentenceTransformer
import torch
import asyncio

class LocalEmbeddingProvider(EmbeddingProvider):

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    async def embed(self, texts: List[str]) -> List[List[float]]:
        loop = asyncio.get_event_loop()
        # Explicitly pass convert_to_numpy=True and avoid positional arguments that might be misinterpreted
        return await loop.run_in_executor(None, lambda: self.model.encode(texts, convert_to_numpy=True).tolist())

    async def health_check(self) -> bool:
        try:
            _ = await self.embed(["health check"])
            return True
        except Exception:
            return False