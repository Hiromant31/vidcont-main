"""
Render Schema - Data models for render server integration
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class JobStatus(str, Enum):
    QUEUED = "queued"
    UPLOADING = "uploading"
    RUNNING = "running"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ServerStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"


@dataclass
class RenderJob:
    """Represents a render job on Colab server"""
    render_job_id: str
    job_id: str
    colab_url: str
    status: JobStatus = JobStatus.QUEUED
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    result_video_url: Optional[str] = None
    logs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "render_job_id": self.render_job_id,
            "job_id": self.job_id,
            "colab_url": self.colab_url,
            "status": self.status.value,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result_video_url": self.result_video_url,
            "logs": self.logs
        }


@dataclass
class ColabServer:
    """Represents a Colab render server"""
    server_id: str
    url: str
    status: ServerStatus = ServerStatus.UNKNOWN
    last_ping: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "server_id": self.server_id,
            "url": self.url,
            "status": self.status.value,
            "last_ping": self.last_ping.isoformat() if self.last_ping else None
        }


@dataclass
class RenderSettings:
    """Render configuration settings"""
    resolution: str
    orientation: str
    fps: int = 30

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resolution": self.resolution,
            "orientation": self.orientation,
            "fps": self.fps
        }


@dataclass
class RenderPayload:
    """Payload sent to Colab for rendering"""
    manifest_file: Dict[str, Any]
    assets: List[str]
    subtitles_file: str
    ffmpeg_script: str
    settings: RenderSettings

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifest_file": self.manifest_file,
            "assets": self.assets,
            "subtitles_file": self.subtitles_file,
            "ffmpeg_script": self.ffmpeg_script,
            "settings": self.settings.to_dict()
        }


@dataclass
class RenderResult:
    """Result of a completed render job"""
    render_job_id: str
    video_path: str
    duration_sec: float
    resolution: str
    status: str  # "success" | "failed"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "render_job_id": self.render_job_id,
            "video_path": self.video_path,
            "duration_sec": self.duration_sec,
            "resolution": self.resolution,
            "status": self.status
        }
