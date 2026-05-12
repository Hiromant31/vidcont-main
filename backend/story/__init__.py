"""
Story + Script System

Central module for story generation, adaptation, and script building.
Exports all components for easy importing.
"""

from .story_schema import (
    Story,
    AdaptedStory,
    Scene,
    NarrativeStructure,
    StyleInfo,
    GenerateStoryInput,
    AdaptStoryInput,
    BuildScriptInput,
    SplitScenesInput,
    ParseNarrativeInput,
    ExtractStyleInput,
    StoryError,
    STORY_TOO_LONG_ERROR,
    INVALID_SCENE_SPLIT_ERROR,
)

from .story_generator import StoryGenerator
from .story_adapter import StoryAdapter
from .script_builder import ScriptBuilder
from .scene_splitter import SceneSplitter
from .narrative_parser import NarrativeParser
from .style_extractor import StyleExtractor


__all__ = [
    # Schemas
    "Story",
    "AdaptedStory",
    "Scene",
    "NarrativeStructure",
    "StyleInfo",
    "GenerateStoryInput",
    "AdaptStoryInput",
    "BuildScriptInput",
    "SplitScenesInput",
    "ParseNarrativeInput",
    "ExtractStyleInput",
    "StoryError",
    "STORY_TOO_LONG_ERROR",
    "INVALID_SCENE_SPLIT_ERROR",
    # Classes
    "StoryGenerator",
    "StoryAdapter",
    "ScriptBuilder",
    "SceneSplitter",
    "NarrativeParser",
    "StyleExtractor",
]
