# app/domain/models.py

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class VectorPoint(BaseModel):
    id: str = Field(..., description="Unique vector ID")
    vector: List[float] = Field(..., description="Embedding vector")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    namespace: Optional[str] = None


class SearchQuery(BaseModel):
    vector: List[float]
    top_k: int = 5
    filters: Optional[Dict[str, Any]] = None
    namespace: Optional[str] = None


class SearchResult(BaseModel):
    id: str
    score: float
    metadata: Dict[str, Any]
    namespace: Optional[str] = None
