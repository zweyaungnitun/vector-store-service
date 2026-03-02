from app.embeddings.base import EmbeddingProvider
from openai import AsyncOpenAI
from typing import List
class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
    ):
        self.client = AsyncOpenAI(api_key=api_key),
        self.model = model

    async def embed(self,text :List[str])->List[List[float]]:
        response = await self.client.embeddings.create(
            model = self.model,
            input=texts,
        )

        return [item.embedding for item in response.data]

    async def health_check(self) -> bool:
        try:
            await self.client.embeddings.create(
                model=self.model,
                input=["health check"],
            )
            return True
        except Exception:
            return False