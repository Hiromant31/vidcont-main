"""
Manifest API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from api.schemas.manifest_schema import (
    BuildManifestRequest,
    ManifestResponse,
    CalculateTimelineRequest,
    TimelineResponse,
    MapTransitionsRequest,
    TransitionsResponse,
    BuildFFmpegScriptRequest,
    FFmpegScriptResponse,
    PackageRenderRequest,
    RenderPackageResponse,
)
from manifest.manifest_builder import ManifestBuilder
from manifest.timeline_calculator import TimelineCalculator
from manifest.transition_mapper import TransitionMapper
from manifest.ffmpeg_instruction_builder import FFmpegInstructionBuilder
from manifest.export_packager import ExportPackager

router = APIRouter()

# Initialize modules
manifest_builder = ManifestBuilder()
timeline_calculator = TimelineCalculator()
transition_mapper = TransitionMapper()
ffmpeg_builder = FFmpegInstructionBuilder()
export_packager = ExportPackager()


@router.post("/build", response_model=ManifestResponse, tags=["Manifest"])
async def build_manifest(request: BuildManifestRequest):
    """
    Build a complete render manifest from scenes, audio, and subtitles.
    
    Combines all pipeline outputs into a single manifest for rendering.
    """
    try:
        manifest = manifest_builder.build_manifest(
            scenes=request.scenes,
            scene_audio=request.scene_audio,
            subtitles=request.subtitles,
            orientation=request.orientation,
            resolution=request.resolution,
            job_id=request.job_id,
            background_music=request.background_music
        )
        
        return ManifestResponse(
            job_id=manifest.job_id,
            orientation=manifest.orientation,
            resolution=manifest.resolution,
            total_duration_sec=manifest.total_duration_sec,
            scenes=[scene.model_dump() for scene in manifest.scenes],
            subtitles=[sub.model_dump() for sub in manifest.subtitles],
            audio_tracks=manifest.audio_tracks,
            background_music=manifest.background_music,
            transitions=[t.model_dump() if hasattr(t, 'model_dump') else t for t in manifest.transitions]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Manifest building failed: {str(e)}")


@router.post("/calculate-timeline", response_model=TimelineResponse, tags=["Manifest"])
async def calculate_timeline(request: CalculateTimelineRequest):
    """
    Calculate timeline from scene audio data.
    
    Determines start/end times and durations for each scene.
    """
    try:
        result = timeline_calculator.calculate_timeline(request.scene_audio)
        
        return TimelineResponse(
            timed_scenes=[ts.model_dump() if hasattr(ts, 'model_dump') else ts for ts in result.get("timed_scenes", [])],
            total_duration=result.get("total_duration", 0.0),
            scene_durations=result.get("scene_durations", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Timeline calculation failed: {str(e)}")


@router.post("/map-transitions", response_model=TransitionsResponse, tags=["Manifest"])
async def map_transitions(request: MapTransitionsRequest):
    """
    Map transitions between scenes.
    
    Determines appropriate transition types for each scene change.
    """
    try:
        transitions = transition_mapper.map_transitions(request.scenes)
        
        # Create transition map
        transition_map = {
            f"{i}->{i+1}": t.get("type", "cut") 
            for i, t in enumerate(transitions[:-1])
        }
        
        return TransitionsResponse(
            transitions=transitions,
            transition_map=transition_map
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transition mapping failed: {str(e)}")


@router.post("/build-ffmpeg-script", response_model=FFmpegScriptResponse, tags=["Manifest"])
async def build_ffmpeg_script(request: BuildFFmpegScriptRequest):
    """
    Build FFmpeg script from manifest.
    
    Generates FFmpeg commands for video rendering.
    """
    try:
        result = ffmpeg_builder.build_ffmpeg_script(
            request.manifest,
            request.output_path
        )
        
        return FFmpegScriptResponse(
            script=result.get("script", ""),
            commands=result.get("commands", []),
            estimated_processing_time=result.get("estimated_time", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg script building failed: {str(e)}")


@router.post("/package-render", response_model=RenderPackageResponse, tags=["Manifest"])
async def package_render(request: PackageRenderRequest):
    """
    Package render assets and manifest for export.
    
    Organizes all files needed for rendering into a single package.
    """
    try:
        result = export_packager.package_render(
            request.manifest,
            request.assets,
            request.output_dir
        )
        
        return RenderPackageResponse(
            package_path=result.get("package_path", ""),
            manifest_path=result.get("manifest_path", ""),
            assets_count=result.get("assets_count", 0),
            total_size_mb=result.get("total_size_mb", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Render packaging failed: {str(e)}")
