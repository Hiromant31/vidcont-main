"""App Settings schemas for the modular settings module."""
from pydantic import BaseModel, Field
from typing import Optional


class AISettingsSchema(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4"
    api_key: str = ""
    yandex_folder_id: Optional[str] = None
    base_url: Optional[str] = None


class TTSSettingsSchema(BaseModel):
    provider: str = "openai"
    voice: str = "alloy"
    speed: float = 1.0
    pitch: float = 1.0
    emotion: Optional[str] = None


class RenderSettingsSchema(BaseModel):
    resolution: str = "720p"
    orientation: str = "vertical"
    fps: int = 30
    subtitles_enabled: bool = True
    subtitles_style: str = "classic"


class ColabSettingsSchema(BaseModel):
    url: str = "http://localhost:8080"
    is_connected: bool = False
    last_ping: Optional[str] = None


class PipelineDefaultsSchema(BaseModel):
    max_concurrent_jobs: int = 3
    auto_retry_failed: bool = True
    default_duration_sec: int = 60


class AppSettingsRequest(BaseModel):
    ai: AISettingsSchema = AISettingsSchema()
    tts: TTSSettingsSchema = TTSSettingsSchema()
    render: RenderSettingsSchema = RenderSettingsSchema()
    colab: ColabSettingsSchema = ColabSettingsSchema()
    pipeline: PipelineDefaultsSchema = PipelineDefaultsSchema()


class AppSettingsResponse(BaseModel):
    ai: AISettingsSchema
    tts: TTSSettingsSchema
    render: RenderSettingsSchema
    colab: ColabSettingsSchema
    pipeline: PipelineDefaultsSchema
