from app.embeddings.base import EmbeddingProvider


class EmbeddingFactory:

    @staticmethod
    def create(provider: str, **kwargs) -> EmbeddingProvider:
        provider = provider.lower()
        if provider == "openai":
            from app.embeddings.openai import OpenAIEmbeddingProvider

            return OpenAIEmbeddingProvider(
                api_key=kwargs.get("api_key"),
                model=kwargs.get("model_name", "text-embedding-3-small"),
                dimensions=kwargs.get("dimensions", 1024)
            )

        elif provider == "pinecone":
            from app.embeddings.pinecone_inference import PineconeEmbeddingProvider
            
            return PineconeEmbeddingProvider(
                api_key=kwargs.get("api_key"),
                model=kwargs.get("model_name", "multilingual-e5-large")
            )

        elif provider == "local":
            from app.embeddings.local_provider import LocalEmbeddingProvider

            return LocalEmbeddingProvider(
                model_name=kwargs.get("model_name", "all-MiniLM-L6-v2")
            )

        raise ValueError(f"Unsupported embedding provider: {provider}")