from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SkillSchema(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Python"})
    category: Optional[str] = Field(None, json_schema_extra={"example": "Programming Language"})
    level: Optional[str] = Field(None, json_schema_extra={"example": "Advanced"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "General purpose programming"})

class ResumeSchema(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "John Doe"})
    email: Optional[str] = Field(None, json_schema_extra={"example": "john@example.com"})
    experience: str = Field(..., json_schema_extra={"example": "5 years in web dev"})
    years_experience: Optional[int] = Field(None, json_schema_extra={"example": 5})
    skills: List[str] = Field(..., json_schema_extra={"example": ["Python", "FastAPI"]})
    education: Optional[str] = Field(None, json_schema_extra={"example": "BS Computer Science"})

class JobSchema(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "Senior Backend Engineer"})
    description: str = Field(..., json_schema_extra={"example": "Responsible for building APIs"})
    company: str = Field(..., json_schema_extra={"example": "Tech Solutions Inc."})
    location: Optional[str] = Field(None, json_schema_extra={"example": "Remote"})
    skills: List[str] = Field(default_factory=list, json_schema_extra={"example": ["Python", "PostgreSQL"]})

class IngestionResponse(BaseModel):
    id: str
    status: str = "success"

class BulkIngestionResponse(BaseModel):
    ids: List[str]
    count: int
    status: str = "success"
