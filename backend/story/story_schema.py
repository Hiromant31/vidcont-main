"""
Story + Script System Schemas

Entity models for story generation, adaptation, and scene splitting.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Story:
    """Raw generated story from idea."""
    story_id: str
    idea: str
    raw_story: str
    genre: str
    tone: str
    style: str
    duration_target: int
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AdaptedStory:
    """Story adapted for specific duration (e.g., 60 seconds)."""
    story_id: str
    adapted_text: str
    voiceover_script: str
    estimated_duration_sec: int
    scene_count: int


@dataclass
class Scene:
    """Logical scene unit (NOT visual yet)."""
    scene_id: str
    story_id: str
    index: int
    text: str
    voice_text: str
    intent: str
    mood: str
    transition_hint: str


@dataclass
class NarrativeStructure:
    """Classic narrative arc structure."""
    hook: str
    buildup: str
    climax: str
    ending: str


@dataclass
class StyleInfo:
    """Extracted style information from story."""
    tone: str
    mood: str
    visual_style_hint: str


@dataclass
class GenerateStoryInput:
    """Input for StoryGenerator.generate_story."""
    idea: str
    genre: str
    style: str
    channel_id: str


@dataclass
class AdaptStoryInput:
    """Input for StoryAdapter.adapt_story_to_duration."""
    story_id: str
    target_duration_sec: int


@dataclass
class BuildScriptInput:
    """Input for ScriptBuilder.build_voiceover_script."""
    adapted_story_id: str


@dataclass
class SplitScenesInput:
    """Input for SceneSplitter.split_into_scenes."""
    voiceover_script: str
    scene_count: int


@dataclass
class ParseNarrativeInput:
    """Input for NarrativeParser.parse_structure."""
    story_text: str


@dataclass
class ExtractStyleInput:
    """Input for StyleExtractor.extract_style."""
    story_text: str


# Error types
@dataclass
class StoryError:
    """Base error for story system."""
    error: str
    action: Optional[str] = None
    fallback: Optional[str] = None


STORY_TOO_LONG_ERROR = StoryError(
    error="STORY_TOO_LONG",
    action="force_adapt"
)

INVALID_SCENE_SPLIT_ERROR = StoryError(
    error="INVALID_SCENE_SPLIT",
    fallback="equal_split"
)
