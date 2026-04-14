from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any
from app.domain.interfaces import VectorStore

class PineconeStore(VectorStore):
    def __init__(
        self,
        api_key: str,
        environment: str,
        index_name: str,
        dimension: int = 384  # Default for all-MiniLM-L6-v2
    ):
        try:
            self.pc = Pinecone(api_key=api_key)
            self.index_name = index_name
            self.dimension = dimension
            
            existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                print(f"Index '{self.index_name}' does not exist. Creating it...")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=environment
                    )
                )
                
            self.index = self.pc.Index(self.index_name)
        except Exception as e:
            print(f"Error initializing Pinecone: {str(e)}")
            # We don't raise here to allow the factory to return the object, 
            # but subsequent calls will fail with a clearer message.
            self.index = None

    async def upsert(
        self,
        collection: str,
        ids: List[str],
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]]
    ) -> None:
        """
        Upserts vectors to Pinecone. We map collection name to a Pinecone namespace.
        """
        if self.index is None:
            raise ConnectionError("Pinecone index is not initialized.")

        # Limit for metadata strings to avoid Pinecone's 40KB payload limit per record
        MAX_STR_LEN = 1000 

        # Format for pinecone: list of tuples (id, vector, metadata)
        vectors_to_upsert = []
        for i in range(len(ids)):
            # Pinecone metadata must be flat. Nested dicts are not allowed.
            clean_meta = {}
            for k, v in metadata[i].items():
                if v is None:
                    continue
                
                # Check value type and size
                if isinstance(v, (int, float, bool)):
                    clean_meta[k] = v
                elif isinstance(v, str):
                    # Truncate long strings to stay within size limits
                    clean_meta[k] = v[:MAX_STR_LEN] if len(v) > MAX_STR_LEN else v
                elif isinstance(v, list) and all(isinstance(x, str) for x in v):
                    # Lists of strings are allowed, but we should also check total length if needed
                    clean_meta[k] = v
                else:
                    # Stringify and truncate nested objects or non-primitive types
                    str_v = str(v)
                    clean_meta[k] = str_v[:MAX_STR_LEN] if len(str_v) > MAX_STR_LEN else str_v
                    
            vectors_to_upsert.append((ids[i], vectors[i], clean_meta))
            
        # Chunk the upserts as Pinecone has limited request sizes
        batch_size = 100
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i+batch_size]
            self.index.upsert(vectors=batch, namespace=collection)

    async def search(
        self,
        collection: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Dict[str, Any] | None = None
    ) -> List[Dict[str, Any]]:
        """
        Searches vectors in Pinecone. Maps collection name to a Pinecone namespace.
        """
        response = self.index.query(
            vector=query_vector,
            top_k=top_k,
            filter=filters,
            namespace=collection,
            include_metadata=True
        )
        
        output = []
        for match in response.get("matches", []):
            output.append({
                "id": match.get("id"),
                "score": match.get("score"),
                "metadata": match.get("metadata", {}),
            })
            
        return output

    async def delete(self, collection: str, ids: List[str]) -> None:
        """
        Deletes vectors from Pinecone. Maps collection name to a Pinecone namespace.
        """
        self.index.delete(ids=ids, namespace=collection)
