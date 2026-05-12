"""
Settings API Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CreateSettingsRequest(BaseModel):
    """Request for creating new settings"""
    settings_id: str
    ai_provider: str = Field(..., description="openai | yandex | other")
    model: str
    api_key: str
    folder_id: Optional[str] = None
    default_quality: str = Field("720", description="240 | 360 | 480 | 720 | 1080")
    auto_continue_pipeline: bool = True


class SettingsResponse(BaseModel):
    """Settings response"""
    settings_id: str
    ai_provider: str
    model: str
    api_key: str
    folder_id: Optional[str]
    default_quality: str
    auto_continue_pipeline: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UpdateSettingsRequest(BaseModel):
    """Partial update for settings"""
    ai_provider: Optional[str] = None
    model: Optional[str] = None
    api_key: Optional[str] = None
    folder_id: Optional[str] = None
    default_quality: Optional[str] = None
    auto_continue_pipeline: Optional[bool] = None


class CreateChannelRequest(BaseModel):
    """Request for creating a channel"""
    channel_id: str
    name: str
    description: str
    target_audience: str
    content_type: str
    settings_id: str


class ChannelResponse(BaseModel):
    """Channel response"""
    channel_id: str
    name: str
    description: str
    target_audience: str
    content_type: str
    settings_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class GetPromptPackRequest(BaseModel):
    """Request for getting prompt pack"""
    pack_type: str = Field(..., description="story | character | scene | style")
    genre: Optional[str] = None
    style: Optional[str] = None
    version: Optional[str] = None


class PromptPackResponse(BaseModel):
    """Prompt pack response"""
    pack_type: str
    prompts: List[Dict[str, Any]]
    variables: List[str]
    version: str


class RenderPromptRequest(BaseModel):
    """Request for rendering a prompt template"""
    template_id: str
    variables: Dict[str, Any]
    version: Optional[str] = None


class RenderedPromptResponse(BaseModel):
    """Rendered prompt response"""
    template_id: str
    rendered_prompt: str
    variables_used: List[str]


class ResolveVariablesRequest(BaseModel):
    """Request for resolving variables in template"""
    template: str
    context: Dict[str, Any]


class VariablesResolutionResponse(BaseModel):
    """Variables resolution response"""
    resolved_template: str
    unresolved_variables: List[str]
