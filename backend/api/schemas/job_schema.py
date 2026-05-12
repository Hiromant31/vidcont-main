"""
Схемы данных для Jobs
Pydantic модели для API
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class JobStatus:
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class JobCreate(BaseModel):
    project_id: str
    idea: str
    genre: str = "general"
    style: str = "cinematic"
    duration_target: int = 60
    orientation: str = "vertical"
    resolution: str = "720p"

class JobResponse(BaseModel):
    job_id: str
    project_id: str
    status: str
    current_stage: Optional[str]
    progress: float
    created_at: datetime
    updated_at: datetime
    logs: List[str]
    errors: List[str]

class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int

class JobUpdateRequest(BaseModel):
    status: Optional[str] = None
    current_stage: Optional[str] = None
    progress: Optional[float] = None
