"""
Settings Schema Module

Defines all data schemas for the Settings + Prompt System.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Settings:
    """AI Provider and pipeline configuration settings."""
    settings_id: str
    ai_provider: str  # "openai" | "yandex" | "other"
    model: str
    api_key: str
    folder_id: Optional[str]
    default_quality: str  # "240" | "360" | "480" | "720" | "1080"
    auto_continue_pipeline: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class Channel:
    """Content channel configuration."""
    channel_id: str
    name: str
    genre: str
    style: str
    settings_id: str
    default_prompt_pack_id: str


@dataclass
class PromptTemplate:
    """Prompt template for a specific stage."""
    template_id: str
    name: str
    stage: str  # One of the valid stage names
    content: str
    variables: List[str]
    version: int
    channel_id: str
    created_at: datetime
    updated_at: datetime


@dataclass
class PromptPack:
    """Collection of prompt templates for a channel."""
    pack_id: str
    channel_id: str
    story_prompt_id: str
    character_prompt_id: str
    scene_prompt_id: str
    storyboard_prompt_id: str
    metadata_prompt_id: str


@dataclass
class VariableSet:
    """Runtime input variables for prompt rendering."""
    duration: int
    episode_count: int
    orientation: str  # "vertical" | "horizontal" | "square"
    genre: str
    style: str
    mood: str
    channel_name: str


@dataclass
class ProviderConfig:
    """AI Provider configuration for API calls."""
    provider_name: str
    api_key: str
    base_url: str
    model: str
    folder_id: Optional[str]
