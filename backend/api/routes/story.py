"""
Story API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from api.schemas.story_schema import (
    GenerateStoryRequest,
    StoryResponse,
    ParseNarrativeRequest,
    NarrativeStructureResponse,
    SplitScenesRequest,
    ScenesResponse,
    BuildScriptRequest,
    ScriptResponse,
    AdaptStoryRequest,
    StyleExtractRequest,
)
from story.story_generator import StoryGenerator
from story.narrative_parser import NarrativeParser
from story.scene_splitter import SceneSplitter
from story.script_builder import ScriptBuilder
from story.story_adapter import StoryAdapter
from story.style_extractor import StyleExtractor

router = APIRouter()

# Initialize modules
story_generator = StoryGenerator()
narrative_parser = NarrativeParser()
scene_splitter = SceneSplitter()
script_builder = ScriptBuilder()
story_adapter = StoryAdapter()
style_extractor = StyleExtractor()


@router.post("/generate", response_model=StoryResponse, tags=["Story"])
async def generate_story(request: GenerateStoryRequest):
    """
    Generate a story from an idea.
    
    Creates a raw story based on the provided idea, genre, style, and channel settings.
    """
    try:
        input_data = {
            "idea": request.idea,
            "genre": request.genre,
            "style": request.style,
            "channel_id": request.channel_id
        }
        
        story = story_generator.generate_story(input_data)
        
        return StoryResponse(
            story_id=story.story_id,
            idea=story.idea,
            raw_story=story.raw_story,
            genre=story.genre,
            tone=story.tone,
            style=story.style,
            duration_target=story.duration_target,
            created_at=story.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")


@router.post("/parse-narrative", response_model=NarrativeStructureResponse, tags=["Story"])
async def parse_narrative(request: ParseNarrativeRequest):
    """
    Parse narrative structure from a raw story.
    
    Extracts acts, key events, climax, and resolution from the story.
    """
    try:
        structure = narrative_parser.parse_structure(request.raw_story)
        
        return NarrativeStructureResponse(
            story_id=request.story_id,
            acts=structure.get("acts", []),
            key_events=structure.get("key_events", []),
            climax_point=structure.get("climax_point", ""),
            resolution=structure.get("resolution", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Narrative parsing failed: {str(e)}")


@router.post("/split-scenes", response_model=ScenesResponse, tags=["Story"])
async def split_scenes(request: SplitScenesRequest):
    """
    Split story into individual scenes.
    
    Divides the narrative structure into discrete scenes for video generation.
    """
    try:
        scenes = scene_splitter.split_into_scenes(
            request.narrative_structure,
            request.target_scene_count
        )
        
        return ScenesResponse(
            story_id=request.story_id,
            scenes=scenes,
            total_scenes=len(scenes)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scene splitting failed: {str(e)}")


@router.post("/build-script", response_model=ScriptResponse, tags=["Story"])
async def build_script(request: BuildScriptRequest):
    """
    Build voiceover script from scenes.
    
    Creates narrated voiceover text for each scene.
    """
    try:
        result = script_builder.build_voiceover_script(
            request.scenes,
            request.style,
            request.tone
        )
        
        return ScriptResponse(
            script=result.get("script", ""),
            scene_scripts=result.get("scene_scripts", []),
            total_duration_estimate=result.get("duration", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script building failed: {str(e)}")


@router.post("/adapt-duration", tags=["Story"])
async def adapt_duration(request: AdaptStoryRequest):
    """
    Adapt story to fit target duration.
    
    Adjusts scene count and content to match the desired video length.
    """
    try:
        adapted = story_adapter.adapt_story_to_duration(
            request.story_id,
            request.current_duration,
            request.target_duration
        )
        
        return {
            "story_id": request.story_id,
            "original_duration": request.current_duration,
            "target_duration": request.target_duration,
            "adapted_scenes": adapted.get("scenes", []),
            "adjustments": adapted.get("adjustments", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Duration adaptation failed: {str(e)}")


@router.post("/extract-style", tags=["Story"])
async def extract_style(request: StyleExtractRequest):
    """
    Extract visual/narrative style from story.
    
    Analyzes story to determine consistent style parameters.
    """
    try:
        style = style_extractor.extract_style(
            request.raw_story,
            request.genre
        )
        
        return {
            "story_id": request.story_id,
            "visual_style": style.get("visual_style", ""),
            "color_palette": style.get("color_palette", []),
            "mood": style.get("mood", ""),
            "lighting": style.get("lighting", ""),
            "composition": style.get("composition", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Style extraction failed: {str(e)}")
