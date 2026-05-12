"""
Схемы данных для Pipeline
Pydantic модели для API
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class StageStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class PipelineStage(BaseModel):
    name: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class PipelineRunRequest(BaseModel):
    job_id: str
    stages: Optional[List[str]] = None

class PipelineStageRequest(BaseModel):
    job_id: str
    stage: str

class PipelineResponse(BaseModel):
    job_id: str
    status: str
    current_stage: Optional[str]
    stages: List[PipelineStage]
    progress: float
    created_at: datetime
    updated_at: datetime

class StageProgress(BaseModel):
    stage: str
    progress: float
    message: Optional[str] = None
