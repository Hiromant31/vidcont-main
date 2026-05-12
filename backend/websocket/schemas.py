"""WebSocket Message Schemas — единая спецификация событий"""
from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from datetime import datetime


class WSBaseMessage(BaseModel):
    type: str
    data: dict
    timestamp: str


# --- Job события ---

class JobStartedData(BaseModel):
    job_id: str
    project_id: str
    status: str = "queued"
    created_at: str


class JobProgressData(BaseModel):
    job_id: str
    progress: float
    current_stage: Optional[str] = None


class JobCompletedData(BaseModel):
    job_id: str
    result: Optional[dict] = None


class JobFailedData(BaseModel):
    job_id: str
    error: str
    stage: Optional[str] = None


# --- Pipeline события ---

class StageCompletedData(BaseModel):
    job_id: str
    stage_name: str
    output: Optional[dict] = None


class StageFailedData(BaseModel):
    job_id: str
    stage_name: str
    error: str


# --- Render события ---

class RenderStartedData(BaseModel):
    render_job_id: str
    job_id: str
    status: str = "uploading"


class RenderCompletedData(BaseModel):
    render_job_id: str
    video_url: str


# --- Logs ---

class LogsUpdatedData(BaseModel):
    job_id: str
    logs: List[str]


# --- Metrics ---

class MetricsUpdatedData(BaseModel):
    cpu_usage: float
    memory_usage: float
    active_connections: int
    queue_size: int
    throughput_per_min: float


class ErrorSpikeData(BaseModel):
    metric: str
    value: float
    threshold: float
    message: str


# --- Asset события ---

class AssetEventData(BaseModel):
    id: str
    project_id: str
    type: str
    url: str
    status: str
    name: Optional[str] = None
    thumbnail_url: Optional[str] = None
    size_bytes: Optional[int] = None
    error: Optional[str] = None


class AssetDeletedData(BaseModel):
    asset_id: str
