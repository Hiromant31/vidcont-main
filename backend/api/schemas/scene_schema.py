"""
Scenes API Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class BuildSceneRequest(BaseModel):
    """Request for building a scene"""
    scene_text: str
    characters: List[Dict[str, Any]]
    style_profile: Dict[str, Any]
    story_id: str = ""
    index: int = 0
    mood: str = ""


class SceneResponse(BaseModel):
    """Built scene response"""
    scene_id: str
    story_id: str
    index: int
    voice_text: str
    visual_prompt: str
    characters: List[str]
    mood: str
    style: str
    camera_motion: str
    transition: str
    estimated_duration_sec: Optional[float]
    subtitle_text: str
    
    class Config:
        from_attributes = True


class SplitScriptRequest(BaseModel):
    """Request for splitting script into scenes"""
    script: str
    target_scene_count: Optional[int] = None
    style: str = ""


class ScriptScenesResponse(BaseModel):
    """Script split into scenes"""
    scenes: List[dict]
    total_scenes: int
    estimated_total_duration: float


class EstimateDurationRequest(BaseModel):
    """Request for estimating scene duration"""
    scene_text: str
    speech_rate: Optional[float] = Field(1.0, description="Speech rate multiplier")


class DurationEstimateResponse(BaseModel):
    """Estimated duration"""
    scene_text: str
    estimated_duration_sec: float
    word_count: int
    speech_rate: float


class GenerateMotionRequest(BaseModel):
    """Request for generating camera motion"""
    scene_id: str
    scene_data: Dict[str, Any]
    mood: str
    intensity: str = Field("medium", description="low | medium | high")


class MotionResponse(BaseModel):
    """Generated camera motion"""
    scene_id: str
    camera_motion: str
    motion_parameters: Dict[str, Any]
    duration_sec: float


class GenerateTransitionRequest(BaseModel):
    """Request for generating transition"""
    current_scene: Dict[str, Any]
    next_scene: Dict[str, Any]
    transition_style: Optional[str] = None


class TransitionResponse(BaseModel):
    """Generated transition"""
    transition_type: str
    transition_duration: float
    transition_parameters: Dict[str, Any]


class BuildVisualPromptRequest(BaseModel):
    """Request for building visual prompt"""
    scene_data: Dict[str, Any]
    characters: List[Dict[str, Any]]
    style_profile: Dict[str, Any]


class VisualPromptResponse(BaseModel):
    """Built visual prompt"""
    scene_id: str
    visual_prompt: str
    negative_prompt: str
    style_directives: List[str]
