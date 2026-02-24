from app.embeddings.openai import OpenAIEmbeddingProvider
from app.embeddings.base import EmbeddingProvider
class EmbeddingFactory:
    def create(provider: str, **kwargs) -> EmbeddingProvider:
        if provider == "openai":
            return OpenAIEmbeddingProvider(
                api_key=kwargs.get("api_key"),
                model=kwargs.get("model", "text-embedding-3-small"),
            )
        elif provider == "local":
            return LocalEmbeddingProvider(
                model_name=kwargs.get("model_name", "all-MiniLM-L6-v2")
            )

        raise ValueError(f"Unsupported embedding provider: {provider}")