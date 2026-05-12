"""
Characters API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from api.schemas.character_schema import (
    ExtractCharactersRequest,
    CharacterSetResponse,
    CharacterResponse,
    BuildCharacterPromptRequest,
    CharacterPromptResponse,
    LockIdentityRequest,
    IdentityLockResponse,
    GenerateReferenceRequest,
    ReferenceImageResponse,
    NormalizeStyleRequest,
    StyleNormalizationResponse,
    BuildScenePromptRequest,
    ScenePromptResponse,
)
from characters.character_extractor import CharacterExtractor
from characters.character_builder import CharacterBuilder
from characters.consistency_manager import ConsistencyManager
from characters.reference_generator import ReferenceGenerator
from characters.style_normalizer import StyleNormalizer
from characters.prompt_builder import PromptBuilder

router = APIRouter()

# Initialize modules
character_extractor = CharacterExtractor()
character_builder = CharacterBuilder()
consistency_manager = ConsistencyManager()
reference_generator = ReferenceGenerator()
style_normalizer = StyleNormalizer()
prompt_builder = PromptBuilder()


@router.post("/extract", response_model=CharacterSetResponse, tags=["Characters"])
async def extract_characters(request: ExtractCharactersRequest):
    """
    Extract characters from story text.
    
    Analyzes the story and identifies main characters (max 3 by default).
    """
    try:
        character_set = character_extractor.extract_characters(
            request.story_text,
            request.max_characters
        )
        
        # Set story_id on the set and characters
        character_set.story_id = request.story_id
        for char in character_set.characters:
            char.story_id = request.story_id
        
        return CharacterSetResponse(
            set_id=character_set.set_id,
            story_id=request.story_id,
            characters=[
                CharacterResponse(
                    character_id=char.character_id,
                    name=char.name,
                    type=char.type,
                    description=char.description,
                    visual_prompt=char.visual_prompt,
                    role=char.role,
                    consistency_tag=char.consistency_tag
                )
                for char in character_set.characters
            ],
            max_count=character_set.max_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Character extraction failed: {str(e)}")


@router.post("/build-prompt", response_model=CharacterPromptResponse, tags=["Characters"])
async def build_character_prompt(request: BuildCharacterPromptRequest):
    """
    Build detailed visual prompt for a character.
    
    Creates a comprehensive prompt for image generation based on character data and style.
    """
    try:
        result = character_builder.build_character_prompt(
            request.character,
            request.style_profile,
            request.scene_context
        )
        
        return CharacterPromptResponse(
            character_id=request.character.get("character_id", ""),
            visual_prompt=result.get("prompt", ""),
            style_notes=result.get("style_notes", ""),
            reference_image_prompt=result.get("reference_prompt", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Character prompt building failed: {str(e)}")


@router.post("/lock-identity", response_model=IdentityLockResponse, tags=["Characters"])
async def lock_character_identity(request: LockIdentityRequest):
    """
    Lock character identity for consistency across scenes.
    
    Ensures character appearance remains consistent throughout the video.
    """
    try:
        result = consistency_manager.lock_character_identity(
            request.character_id,
            request.reference_images,
            request.lock_level
        )
        
        return IdentityLockResponse(
            character_id=request.character_id,
            lock_status=result.get("status", "locked"),
            consistency_tag=result.get("consistency_tag", ""),
            locked_features=result.get("locked_features", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Identity locking failed: {str(e)}")


@router.post("/generate-reference", response_model=ReferenceImageResponse, tags=["Characters"])
async def generate_reference_image(request: GenerateReferenceRequest):
    """
    Generate reference image for a character.
    
    Creates a reference image to maintain character consistency.
    """
    try:
        result = reference_generator.generate_reference_image(
            request.character_id,
            request.character_data,
            request.view_angle,
            request.expression
        )
        
        return ReferenceImageResponse(
            character_id=request.character_id,
            image_path=result.get("image_path", ""),
            prompt_used=result.get("prompt", ""),
            view_angle=request.view_angle,
            expression=request.expression
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reference image generation failed: {str(e)}")


@router.post("/normalize-style", response_model=StyleNormalizationResponse, tags=["Characters"])
async def normalize_style(request: NormalizeStyleRequest):
    """
    Normalize character styles to match target style profile.
    
    Adjusts all characters to have consistent visual style.
    """
    try:
        result = style_normalizer.normalize_style(
            request.characters,
            request.target_style
        )
        
        return StyleNormalizationResponse(
            normalized_characters=result.get("normalized_characters", []),
            style_adjustments=result.get("adjustments", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Style normalization failed: {str(e)}")


@router.post("/build-scene-prompt", response_model=ScenePromptResponse, tags=["Characters"])
async def build_scene_prompt(request: BuildScenePromptRequest):
    """
    Build scene prompt including characters.
    
    Creates a comprehensive visual prompt for scene generation with characters.
    """
    try:
        result = prompt_builder.build_scene_prompt(
            request.scene_data,
            request.characters,
            request.style_profile
        )
        
        return ScenePromptResponse(
            scene_id=request.scene_data.get("scene_id", ""),
            visual_prompt=result.get("scene_prompt", ""),
            character_prompts=result.get("character_prompts", []),
            style_directives=result.get("style_directives", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scene prompt building failed: {str(e)}")
