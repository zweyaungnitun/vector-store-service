from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

from app.api.schemas import (
    SkillSchema, 
    ResumeSchema, 
    JobSchema, 
    IngestionResponse, 
    BulkIngestionResponse
)
from app.api.deps import get_skill_ingestor, get_resume_ingestor, get_job_ingestor
from app.ingestion.skill_ingestor import SkillIngestor
from app.ingestion.resume_ingestor import ResumeIngestor
from app.ingestion.job_ingestor import JobIngestor
from app.core.exceptions import ValidationError
from fastapi import File, UploadFile, Query
from app.utils.file_processor import FileProcessor

router = APIRouter(prefix="/ingest", tags=["ingestion"])

@router.post("/skill", response_model=IngestionResponse)
async def ingest_skill(
    skill: SkillSchema,
    ingestor: SkillIngestor = Depends(get_skill_ingestor)
):
    try:
        skill_id = await ingestor.ingest_skill(skill.model_dump())
        return IngestionResponse(id=skill_id)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/resume", response_model=IngestionResponse)
async def ingest_resume(
    resume: ResumeSchema,
    ingestor: ResumeIngestor = Depends(get_resume_ingestor)
):
    try:
        resume_id = await ingestor.ingest_resume(resume.model_dump())
        return IngestionResponse(id=resume_id)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/job", response_model=IngestionResponse)
async def ingest_job(
    job: JobSchema,
    ingestor: JobIngestor = Depends(get_job_ingestor)
):
    try:
        job_id = await ingestor.ingest_job(job.model_dump())
        return IngestionResponse(id=job_id)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/skills/bulk", response_model=BulkIngestionResponse)
async def ingest_bulk_skills(
    skills: List[SkillSchema],
    ingestor: SkillIngestor = Depends(get_skill_ingestor)
):
    try:
        skill_ids = await ingestor.ingest_bulk_skills([s.model_dump() for s in skills])
        return BulkIngestionResponse(ids=skill_ids, count=len(skill_ids))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/resumes/bulk", response_model=BulkIngestionResponse)
async def ingest_bulk_resumes(
    resumes: List[ResumeSchema],
    ingestor: ResumeIngestor = Depends(get_resume_ingestor)
):
    try:
        resume_ids = await ingestor.ingest_bulk_resumes([r.model_dump() for r in resumes])
        return BulkIngestionResponse(ids=resume_ids, count=len(resume_ids))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/jobs/bulk", response_model=BulkIngestionResponse)
async def ingest_bulk_jobs(
    jobs: List[JobSchema],
    ingestor: JobIngestor = Depends(get_job_ingestor)
):
    try:
        job_ids = await ingestor.ingest_bulk_jobs([j.model_dump() for j in jobs])
        return BulkIngestionResponse(ids=job_ids, count=len(job_ids))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/file", response_model=BulkIngestionResponse)
async def ingest_file(
    file: UploadFile = File(...),
    target: str = Query(..., enum=["skill", "resume", "job"]),
    skill_ingestor: SkillIngestor = Depends(get_skill_ingestor),
    resume_ingestor: ResumeIngestor = Depends(get_resume_ingestor),
    job_ingestor: JobIngestor = Depends(get_job_ingestor)
):
    content = await file.read()
    try:
        processed_data = FileProcessor.process_file(file.filename, content)
        
        ids = []
        if isinstance(processed_data, list):
            # CSV/Excel list of dicts
            if target == "skill":
                ids = await skill_ingestor.ingest_bulk_skills(processed_data)
            elif target == "resume":
                ids = await resume_ingestor.ingest_bulk_resumes(processed_data)
            elif target == "job":
                ids = await job_ingestor.ingest_bulk_jobs(processed_data)
        else:
            # Single text from PDF/TXT
            if target == "skill":
                ids.append(await skill_ingestor.ingest_skill({"name": file.filename, "description": processed_data}))
            elif target == "resume":
                # Basic mapping for unstructured text
                ids.append(await resume_ingestor.ingest_resume({
                    "name": file.filename, 
                    "experience": processed_data,
                    "skills": [] 
                }))
            elif target == "job":
                ids.append(await job_ingestor.ingest_job({
                    "title": file.filename,
                    "description": processed_data,
                    "company": "Uploaded File"
                }))
        
        return BulkIngestionResponse(ids=ids, count=len(ids))
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
