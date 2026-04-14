from app.embeddings.base import EmbeddingProvider
from openai import AsyncOpenAI
from typing import List
class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        dimensions: int = 1024,
    ):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.dimensions = dimensions

    async def embed(self, texts: List[str]) -> List[List[float]]:
        # text-embedding-3 supports a 'dimensions' parameter for truncation
        # to match specific architectures like 1024 or 512.
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimensions if "text-embedding-3" in self.model else None
        )

        return [item.embedding for item in response.data]

    async def health_check(self) -> bool:
        try:
            await self.client.embeddings.create(
                model=self.model,
                input=["health check"],
                dimensions=self.dimensions if "text-embedding-3" in self.model else None
            )
            return True
        except Exception:
            return False