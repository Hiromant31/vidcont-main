"""
Render API Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class StartRenderRequest(BaseModel):
    """Request for starting a render job"""
    job_id: str
    colab_url: str
    manifest: Dict[str, Any]
    assets: List[str]
    background_music: Optional[str] = None


class RenderJobResponse(BaseModel):
    """Render job status response"""
    render_job_id: str
    job_id: str
    colab_url: str
    status: str  # uploading | running | completed | failed | unknown
    progress: float
    result_video_url: Optional[str]
    logs: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CheckStatusRequest(BaseModel):
    """Request for checking render status"""
    render_job_id: str


class StopRenderRequest(BaseModel):
    """Request for stopping a render job"""
    render_job_id: str


class ConnectServerRequest(BaseModel):
    """Request for connecting to Colab server"""
    colab_url: str
    timeout: int = Field(30, description="Connection timeout in seconds")


class ServerConnectionResponse(BaseModel):
    """Server connection status"""
    connected: bool
    server_info: Dict[str, Any]
    latency_ms: float


class HealthCheckRequest(BaseModel):
    """Request for health check"""
    colab_url: str


class HealthCheckResponse(BaseModel):
    """Health check result"""
    healthy: bool
    gpu_available: bool
    memory_available_gb: float
    disk_available_gb: float
    ffmpeg_version: str


class UploadAssetsRequest(BaseModel):
    """Request for uploading assets"""
    colab_url: str
    assets: List[str]
    asset_type: str = Field("image", description="image | audio | video | other")


class UploadResultResponse(BaseModel):
    """Upload result"""
    uploaded_count: int
    uploaded_paths: List[str]
    failed_uploads: List[dict]
    total_size_mb: float


class DownloadResultRequest(BaseModel):
    """Request for downloading render result"""
    render_job_id: str
    colab_url: str
    output_path: str
