from app.embeddings.base import EmbeddingProvider


class EmbeddingFactory:

    @staticmethod
    def create(provider: str, **kwargs) -> EmbeddingProvider:

        if provider == "openai":
            from app.embeddings.openai import OpenAIEmbeddingProvider

            return OpenAIEmbeddingProvider(
                api_key=kwargs.get("api_key"),
                model=kwargs.get("model", "text-embedding-3-small"),
            )

        elif provider == "local":
            from app.embeddings.local_provider import LocalEmbeddingProvider

            return LocalEmbeddingProvider(
                model_name=kwargs.get("model_name", "all-MiniLM-L6-v2")
            )

        raise ValueError(f"Unsupported embedding provider: {provider}")