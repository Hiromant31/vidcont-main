"""
Pipeline control endpoints
"""
from fastapi import APIRouter, HTTPException
from api.schemas.pipeline_schema import PipelineRunRequest, PipelineStageRequest, PipelineResponse
from orchestration.pipeline_manager import PipelineManager

router = APIRouter()
pipeline_manager = PipelineManager()

@router.post("/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRunRequest):
    """Запустить полный пайплайн для задачи"""
    job = pipeline_manager.run_pipeline(request.job_id, request.stages)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/run-stage", response_model=PipelineResponse)
async def run_stage(request: PipelineStageRequest):
    """Запустить конкретный этап пайплайна"""
    job = pipeline_manager.run_stage(request.job_id, request.stage)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/pause")
async def pause_pipeline(job_id: str):
    """Поставить пайплайн на паузу"""
    result = pipeline_manager.pause_pipeline(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "paused", "job_id": job_id}

@router.post("/resume")
async def resume_pipeline(job_id: str):
    """Возобновить пайплайн после паузы"""
    result = pipeline_manager.resume_pipeline(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "resumed", "job_id": job_id}
