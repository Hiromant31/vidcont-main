"""
Story API Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class GenerateStoryRequest(BaseModel):
    """Request for generating a story"""
    idea: str = Field(..., description="Story idea/concept")
    genre: str = Field(..., description="Genre of the story")
    style: str = Field(..., description="Visual/narrative style")
    channel_id: str = Field(..., description="Channel ID for settings")
    duration_target: Optional[int] = Field(60, description="Target duration in seconds")


class StoryResponse(BaseModel):
    """Response containing generated story"""
    story_id: str
    idea: str
    raw_story: str
    genre: str
    tone: str
    style: str
    duration_target: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ParseNarrativeRequest(BaseModel):
    """Request for parsing narrative structure"""
    story_id: str
    raw_story: str


class NarrativeStructureResponse(BaseModel):
    """Parsed narrative structure"""
    story_id: str
    acts: List[dict]
    key_events: List[str]
    climax_point: str
    resolution: str


class SplitScenesRequest(BaseModel):
    """Request for splitting story into scenes"""
    story_id: str
    narrative_structure: dict
    target_scene_count: Optional[int] = None


class ScenesResponse(BaseModel):
    """List of scenes from story"""
    story_id: str
    scenes: List[dict]
    total_scenes: int


class BuildScriptRequest(BaseModel):
    """Request for building voiceover script"""
    scenes: List[dict]
    style: str
    tone: str


class ScriptResponse(BaseModel):
    """Generated voiceover script"""
    script: str
    scene_scripts: List[dict]
    total_duration_estimate: float


class AdaptStoryRequest(BaseModel):
    """Request for adapting story to duration"""
    story_id: str
    current_duration: float
    target_duration: float


class StyleExtractRequest(BaseModel):
    """Request for extracting style from story"""
    story_id: str
    raw_story: str
    genre: str
