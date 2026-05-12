"""Asset API Schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AssetType(str, Enum):
    image = "image"
    audio = "audio"
    video = "video"
    subtitle = "subtitle"
    thumbnail = "thumbnail"
    temp = "temp"


class AssetStatus(str, Enum):
    processing = "processing"
    ready = "ready"
    failed = "failed"


class AssetEntityType(str, Enum):
    scene = "scene"
    job = "job"
    render = "render"
    project = "project"


class AssetResponse(BaseModel):
    id: str
    project_id: str
    job_id: Optional[str] = None
    scene_id: Optional[str] = None
    render_id: Optional[str] = None
    type: AssetType
    url: str
    thumbnail_url: Optional[str] = None
    status: AssetStatus
    metadata: Optional[Dict[str, Any]] = None
    size_bytes: Optional[int] = None
    duration_sec: Optional[float] = None
    created_at: datetime
    name: Optional[str] = None

    class Config:
        from_attributes = True


class AssetUsageResponse(BaseModel):
    id: str
    asset_id: str
    entity_type: AssetEntityType
    entity_id: str
    used_at: datetime
    context: Optional[str] = None

    class Config:
        from_attributes = True


class ReuseAssetRequest(BaseModel):
    asset_id: str
    target_entity: Dict[str, str] = Field(
        ...,
        description='{"type": "scene|job|render|project", "id": "entity_id"}'
    )


class DeleteAssetResponse(BaseModel):
    message: str
    asset_id: str
