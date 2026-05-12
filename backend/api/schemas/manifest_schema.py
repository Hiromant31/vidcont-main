"""
Manifest API Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class BuildManifestRequest(BaseModel):
    """Request for building a render manifest"""
    scenes: List[Dict[str, Any]]
    scene_audio: List[Dict[str, Any]]
    subtitles: List[Dict[str, Any]]
    orientation: str = "vertical"
    resolution: str = "720p"
    job_id: Optional[str] = None
    background_music: Optional[str] = None


class ManifestResponse(BaseModel):
    """Built manifest response"""
    job_id: str
    orientation: str
    resolution: str
    total_duration_sec: float
    scenes: List[dict]
    subtitles: List[dict]
    audio_tracks: List[str]
    background_music: Optional[str]
    transitions: List[dict]
    
    class Config:
        from_attributes = True


class CalculateTimelineRequest(BaseModel):
    """Request for calculating timeline"""
    scene_audio: List[Dict[str, Any]]


class TimelineResponse(BaseModel):
    """Calculated timeline"""
    timed_scenes: List[dict]
    total_duration: float
    scene_durations: List[dict]


class MapTransitionsRequest(BaseModel):
    """Request for mapping transitions"""
    scenes: List[Dict[str, Any]]


class TransitionsResponse(BaseModel):
    """Mapped transitions"""
    transitions: List[dict]
    transition_map: Dict[str, str]


class BuildFFmpegScriptRequest(BaseModel):
    """Request for building FFmpeg script"""
    manifest: Dict[str, Any]
    output_path: str


class FFmpegScriptResponse(BaseModel):
    """Generated FFmpeg script"""
    script: str
    commands: List[str]
    estimated_processing_time: float


class PackageRenderRequest(BaseModel):
    """Request for packaging render"""
    manifest: Dict[str, Any]
    assets: List[str]
    output_dir: str


class RenderPackageResponse(BaseModel):
    """Packaged render info"""
    package_path: str
    manifest_path: str
    assets_count: int
    total_size_mb: float
