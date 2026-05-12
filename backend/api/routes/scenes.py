"""
Scenes API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from api.schemas.scene_schema import (
    BuildSceneRequest,
    SceneResponse,
    SplitScriptRequest,
    ScriptScenesResponse,
    EstimateDurationRequest,
    DurationEstimateResponse,
    GenerateMotionRequest,
    MotionResponse,
    GenerateTransitionRequest,
    TransitionResponse,
    BuildVisualPromptRequest,
    VisualPromptResponse,
)
from scenes.scene_builder import SceneBuilder
from scenes.scene_splitter import SceneSplitter
from scenes.timing_estimator import TimingEstimator
from scenes.motion_generator import MotionGenerator
from scenes.transition_builder import TransitionBuilder
from scenes.prompt_builder import PromptBuilder

router = APIRouter()

# Initialize modules
scene_builder = SceneBuilder()
scene_splitter = SceneSplitter()
timing_estimator = TimingEstimator()
motion_generator = MotionGenerator()
transition_builder = TransitionBuilder()
prompt_builder = PromptBuilder()


@router.post("/build", response_model=SceneResponse, tags=["Scenes"])
async def build_scene(request: BuildSceneRequest):
    """
    Build a complete scene from text, characters, and style.
    
    Creates a full scene object with visual prompt and all metadata.
    """
    try:
        scene = scene_builder.build_scene(
            scene_text=request.scene_text,
            characters=request.characters,
            style_profile=request.style_profile,
            story_id=request.story_id,
            index=request.index,
            mood=request.mood
        )
        
        return SceneResponse(
            scene_id=scene.scene_id,
            story_id=scene.story_id,
            index=scene.index,
            voice_text=scene.voice_text,
            visual_prompt=scene.visual_prompt,
            characters=scene.characters,
            mood=scene.mood,
            style=scene.style,
            camera_motion=scene.camera_motion,
            transition=scene.transition,
            estimated_duration_sec=scene.estimated_duration_sec,
            subtitle_text=scene.subtitle_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scene building failed: {str(e)}")


@router.post("/split-script", response_model=ScriptScenesResponse, tags=["Scenes"])
async def split_script_into_scenes(request: SplitScriptRequest):
    """
    Split a voiceover script into individual scenes.
    
    Divides the script into logical segments for video generation.
    """
    try:
        scenes = scene_splitter.split_script_into_scenes(
            request.script,
            request.target_scene_count,
            request.style
        )
        
        # Estimate total duration
        total_duration = sum(
            timing_estimator.estimate_duration(scene.get("voice_text", ""))
            for scene in scenes
        )
        
        return ScriptScenesResponse(
            scenes=scenes,
            total_scenes=len(scenes),
            estimated_total_duration=total_duration
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script splitting failed: {str(e)}")


@router.post("/estimate-duration", response_model=DurationEstimateResponse, tags=["Scenes"])
async def estimate_duration(request: EstimateDurationRequest):
    """
    Estimate duration of a scene based on text.
    
    Calculates how long the voiceover will take to narrate.
    """
    try:
        duration = timing_estimator.estimate_duration(
            request.scene_text,
            request.speech_rate
        )
        
        word_count = len(request.scene_text.split())
        
        return DurationEstimateResponse(
            scene_text=request.scene_text,
            estimated_duration_sec=duration,
            word_count=word_count,
            speech_rate=request.speech_rate or 1.0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Duration estimation failed: {str(e)}")


@router.post("/generate-motion", response_model=MotionResponse, tags=["Scenes"])
async def generate_camera_motion(request: GenerateMotionRequest):
    """
    Generate camera motion for a scene.
    
    Determines appropriate camera movement based on scene mood and content.
    """
    try:
        result = motion_generator.generate_camera_motion(
            request.scene_id,
            request.scene_data,
            request.mood,
            request.intensity
        )
        
        return MotionResponse(
            scene_id=request.scene_id,
            camera_motion=result.get("camera_motion", "static"),
            motion_parameters=result.get("parameters", {}),
            duration_sec=result.get("duration", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Motion generation failed: {str(e)}")


@router.post("/generate-transition", response_model=TransitionResponse, tags=["Scenes"])
async def generate_transition(request: GenerateTransitionRequest):
    """
    Generate transition between two scenes.
    
    Creates smooth transition based on scene content and mood.
    """
    try:
        result = transition_builder.generate_transition(
            request.current_scene,
            request.next_scene,
            request.transition_style
        )
        
        return TransitionResponse(
            transition_type=result.get("transition_type", "cut"),
            transition_duration=result.get("duration", 0.5),
            transition_parameters=result.get("parameters", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transition generation failed: {str(e)}")


@router.post("/build-visual-prompt", response_model=VisualPromptResponse, tags=["Scenes"])
async def build_visual_prompt(request: BuildVisualPromptRequest):
    """
    Build visual prompt for scene generation.
    
    Creates detailed prompt for AI image generation.
    """
    try:
        result = prompt_builder.build_visual_prompt(
            request.scene_data,
            request.characters,
            request.style_profile
        )
        
        return VisualPromptResponse(
            scene_id=request.scene_data.get("scene_id", ""),
            visual_prompt=result.get("prompt", ""),
            negative_prompt=result.get("negative_prompt", ""),
            style_directives=result.get("style_directives", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visual prompt building failed: {str(e)}")
