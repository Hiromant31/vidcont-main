"""
Settings API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from api.schemas.settings_schema import (
    CreateSettingsRequest,
    SettingsResponse,
    UpdateSettingsRequest,
    CreateChannelRequest,
    ChannelResponse,
    GetPromptPackRequest,
    PromptPackResponse,
    RenderPromptRequest,
    RenderedPromptResponse,
    ResolveVariablesRequest,
    VariablesResolutionResponse,
)
from settings.settings_manager import SettingsManager
from settings.channel_manager import ChannelManager
from settings.prompt_manager import PromptManager
from settings.template_engine import TemplateEngine
from settings.variable_resolver import VariableResolver

router = APIRouter()

# Initialize modules with mock storage (replace with real storage in production)
class MockStorage:
    """Mock storage for demo purposes"""
    def __init__(self):
        self._settings = {}
        self._channels = {}
    
    def get_settings(self, settings_id: str):
        return self._settings.get(settings_id)
    
    def save_settings(self, settings):
        self._settings[settings.settings_id] = settings
    
    def delete_settings(self, settings_id: str) -> bool:
        if settings_id in self._settings:
            del self._settings[settings_id]
            return True
        return False
    
    def list_settings(self) -> list:
        return list(self._settings.values())
    
    def get_channel(self, channel_id: str):
        return self._channels.get(channel_id)
    
    def save_channel(self, channel):
        self._channels[channel.channel_id] = channel
    
    def delete_channel(self, channel_id: str) -> bool:
        if channel_id in self._channels:
            del self._channels[channel_id]
            return True
        return False
    
    def list_channels(self) -> list:
        return list(self._channels.values())


mock_storage = MockStorage()
settings_manager = SettingsManager(mock_storage)
channel_manager = ChannelManager(mock_storage)
prompt_manager = PromptManager(mock_storage)
template_engine = TemplateEngine()
variable_resolver = VariableResolver()


@router.post("/create", response_model=SettingsResponse, tags=["Settings"])
async def create_settings(request: CreateSettingsRequest):
    """
    Create new AI provider and pipeline settings.
    """
    try:
        settings = settings_manager.create_settings(
            settings_id=request.settings_id,
            ai_provider=request.ai_provider,
            model=request.model,
            api_key=request.api_key,
            folder_id=request.folder_id,
            default_quality=request.default_quality,
            auto_continue_pipeline=request.auto_continue_pipeline
        )
        
        return SettingsResponse(
            settings_id=settings.settings_id,
            ai_provider=settings.ai_provider,
            model=settings.model,
            api_key=settings.api_key,
            folder_id=settings.folder_id,
            default_quality=settings.default_quality,
            auto_continue_pipeline=settings.auto_continue_pipeline,
            created_at=settings.created_at,
            updated_at=settings.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings creation failed: {str(e)}")


@router.delete("/{settings_id}", tags=["Settings"])
async def delete_settings(settings_id: str):
    """
    Delete settings by ID.
    """
    try:
        result = settings_manager.delete_settings(settings_id)
        if result:
            return {"message": f"Settings '{settings_id}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Settings '{settings_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings deletion failed: {str(e)}")


@router.get("/all", response_model=List[SettingsResponse], tags=["Settings"])
async def list_all_settings():
    """
    List all available settings.
    """
    try:
        settings_list = settings_manager.list_settings()
        return [
            SettingsResponse(
                settings_id=s.settings_id,
                ai_provider=s.ai_provider,
                model=s.model,
                api_key=s.api_key,
                folder_id=s.folder_id,
                default_quality=s.default_quality,
                auto_continue_pipeline=s.auto_continue_pipeline,
                created_at=s.created_at,
                updated_at=s.updated_at
            )
            for s in settings_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list settings: {str(e)}")


@router.get("/", response_model=List[SettingsResponse], tags=["Settings"])
async def get_default_settings():
    """
    Get default settings (returns all settings for now).
    """
    return await list_all_settings()


@router.get("/prompts", response_model=List[Dict[str, Any]], tags=["Settings"])
async def list_prompts():
    """
    List all available prompt packs.
    """
    try:
        # Return mock prompt packs for now
        return [
            {
                "id": "story_basic",
                "name": "Basic Story Prompts",
                "type": "story",
                "genre": "general",
                "style": "narrative",
                "version": "1.0"
            },
            {
                "id": "character_fantasy",
                "name": "Fantasy Character Prompts",
                "type": "character",
                "genre": "fantasy",
                "style": "detailed",
                "version": "1.0"
            },
            {
                "id": "scene_cinematic",
                "name": "Cinematic Scene Prompts",
                "type": "scene",
                "genre": "general",
                "style": "cinematic",
                "version": "1.0"
            }
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list prompts: {str(e)}")


@router.get("/{settings_id}", response_model=SettingsResponse, tags=["Settings"])
async def get_settings_by_id(settings_id: str):
    """
    Get settings by ID.
    """
    try:
        settings = settings_manager.get_settings(settings_id)
        if not settings:
            raise HTTPException(status_code=404, detail=f"Settings '{settings_id}' not found")
        
        return SettingsResponse(
            settings_id=settings.settings_id,
            ai_provider=settings.ai_provider,
            model=settings.model,
            api_key=settings.api_key,
            folder_id=settings.folder_id,
            default_quality=settings.default_quality,
            auto_continue_pipeline=settings.auto_continue_pipeline,
            created_at=settings.created_at,
            updated_at=settings.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")


@router.post("/channel/create", response_model=ChannelResponse, tags=["Settings"])
async def create_channel(request: CreateChannelRequest):
    """
    Create a new channel configuration.
    """
    try:
        channel = channel_manager.create_channel(
            channel_id=request.channel_id,
            name=request.name,
            description=request.description,
            target_audience=request.target_audience,
            content_type=request.content_type,
            settings_id=request.settings_id
        )
        
        return ChannelResponse(
            channel_id=channel.channel_id,
            name=channel.name,
            description=channel.description,
            target_audience=channel.target_audience,
            content_type=channel.content_type,
            settings_id=channel.settings_id,
            created_at=channel.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Channel creation failed: {str(e)}")


@router.post("/prompts/get", response_model=PromptPackResponse, tags=["Settings"])
async def get_prompt_pack(request: GetPromptPackRequest):
    """
    Get a prompt pack by type and filters.
    """
    try:
        result = prompt_manager.get_prompt_pack(
            pack_type=request.pack_type,
            genre=request.genre,
            style=request.style,
            version=request.version
        )
        
        return PromptPackResponse(
            pack_type=result.get("pack_type", ""),
            prompts=result.get("prompts", []),
            variables=result.get("variables", []),
            version=result.get("version", "1.0")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get prompt pack: {str(e)}")


@router.post("/prompts/render", response_model=RenderedPromptResponse, tags=["Settings"])
async def render_prompt(request: RenderPromptRequest):
    """
    Render a prompt template with variables.
    """
    try:
        result = template_engine.render_prompt(
            template_id=request.template_id,
            variables=request.variables,
            version=request.version
        )
        
        return RenderedPromptResponse(
            template_id=request.template_id,
            rendered_prompt=result.get("rendered_prompt", ""),
            variables_used=result.get("variables_used", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prompt rendering failed: {str(e)}")


@router.post("/prompts/resolve-variables", response_model=VariablesResolutionResponse, tags=["Settings"])
async def resolve_variables(request: ResolveVariablesRequest):
    """
    Resolve variables in a template string.
    """
    try:
        result = variable_resolver.resolve(
            template=request.template,
            context=request.context
        )
        
        return VariablesResolutionResponse(
            resolved_template=result.get("resolved_template", ""),
            unresolved_variables=result.get("unresolved", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Variable resolution failed: {str(e)}")
