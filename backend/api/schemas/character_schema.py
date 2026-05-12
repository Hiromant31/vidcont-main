"""
Characters API Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ExtractCharactersRequest(BaseModel):
    """Request for extracting characters from story"""
    story_id: str
    story_text: str
    max_characters: Optional[int] = Field(3, description="Maximum number of characters (default 3)")


class CharacterResponse(BaseModel):
    """Single character response"""
    character_id: str
    name: str
    type: str
    description: str
    visual_prompt: str
    role: str
    consistency_tag: str
    
    class Config:
        from_attributes = True


class CharacterSetResponse(BaseModel):
    """Response containing extracted character set"""
    set_id: str
    story_id: str
    characters: List[CharacterResponse]
    max_count: int


class BuildCharacterPromptRequest(BaseModel):
    """Request for building character prompt"""
    character: Dict[str, Any]
    style_profile: Dict[str, Any]
    scene_context: Optional[str] = None


class CharacterPromptResponse(BaseModel):
    """Generated character prompt"""
    character_id: str
    visual_prompt: str
    style_notes: str
    reference_image_prompt: str


class LockIdentityRequest(BaseModel):
    """Request for locking character identity"""
    character_id: str
    reference_images: List[str]
    lock_level: str = Field("strict", description="strict | moderate | flexible")


class IdentityLockResponse(BaseModel):
    """Character identity lock result"""
    character_id: str
    lock_status: str
    consistency_tag: str
    locked_features: List[str]


class GenerateReferenceRequest(BaseModel):
    """Request for generating reference image"""
    character_id: str
    character_data: Dict[str, Any]
    view_angle: str = "front"
    expression: str = "neutral"


class ReferenceImageResponse(BaseModel):
    """Generated reference image info"""
    character_id: str
    image_path: str
    prompt_used: str
    view_angle: str
    expression: str


class NormalizeStyleRequest(BaseModel):
    """Request for normalizing character style"""
    characters: List[Dict[str, Any]]
    target_style: Dict[str, Any]


class StyleNormalizationResponse(BaseModel):
    """Style normalization result"""
    normalized_characters: List[Dict[str, Any]]
    style_adjustments: List[str]


class BuildScenePromptRequest(BaseModel):
    """Request for building scene prompt with characters"""
    scene_data: Dict[str, Any]
    characters: List[Dict[str, Any]]
    style_profile: Dict[str, Any]


class ScenePromptResponse(BaseModel):
    """Generated scene prompt"""
    scene_id: str
    visual_prompt: str
    character_prompts: List[str]
    style_directives: List[str]
