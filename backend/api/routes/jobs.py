"""
Jobs management endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas.job_schema import JobCreate, JobResponse, JobListResponse
from orchestration.job_manager import JobManager

router = APIRouter()
job_manager = JobManager()

@router.get("", response_model=List[JobResponse])
@router.get("/", response_model=List[JobResponse])
async def get_jobs():
    """Получить список всех задач"""
    jobs = job_manager.get_all_jobs()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Получить задачу по ID"""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/start", response_model=JobResponse)
async def start_job(job_data: JobCreate):
    """Создать и запустить новую задачу"""
    job = job_manager.create_job(
        project_id=job_data.project_id,
        idea=job_data.idea,
        genre=job_data.genre,
        style=job_data.style,
        duration_target=job_data.duration_target,
        orientation=job_data.orientation,
        resolution=job_data.resolution
    )
    # Запуск пайплайна в фоне
    await job_manager.run_pipeline_async(job.job_id)
    return job

@router.post("/{job_id}/stop")
async def stop_job(job_id: str):
    """Остановить задачу"""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_manager.stop_job(job_id)
    return {"status": "stopped", "job_id": job_id}

@router.post("/{job_id}/retry")
async def retry_job(job_id: str):
    """Перезапустить_failed задачу"""
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != "failed":
        raise HTTPException(status_code=400, detail="Can only retry failed jobs")
    
    job_manager.retry_job(job_id)
    return {"status": "retried", "job_id": job_id}
