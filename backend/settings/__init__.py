"""
Settings + Prompt System

Central configuration and prompt management system for AI video generation pipeline.

This module handles:
- AI provider settings
- Content channel configurations
- Prompt templates and packs
- Variable substitution
- Prompt versioning
"""

from .settings_schema import (
    Settings,
    Channel,
    PromptTemplate,
    PromptPack,
    VariableSet,
    ProviderConfig,
)

from .settings_manager import SettingsManager
from .channel_manager import ChannelManager
from .prompt_manager import PromptManager
from .template_engine import TemplateEngine
from .variable_resolver import VariableResolver
from .provider_config import ProviderConfigManager
from .prompt_versioning import PromptVersioning

__all__ = [
    # Schemas
    "Settings",
    "Channel",
    "PromptTemplate",
    "PromptPack",
    "VariableSet",
    "ProviderConfig",
    # Managers
    "SettingsManager",
    "ChannelManager",
    "PromptManager",
    "TemplateEngine",
    "VariableResolver",
    "ProviderConfigManager",
    "PromptVersioning",
]
