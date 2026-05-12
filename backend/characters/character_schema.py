"""
Character System Schema Definitions
Defines data models for character management, reference images, and style profiles.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal


@dataclass
class Character:
    """Represents a single character extracted from the story."""
    character_id: str
    story_id: str
    name: str
    type: Literal["human", "group", "creature", "object", "abstract"]
    description: str
    visual_prompt: str
    role: Literal["main", "secondary", "background"]
    consistency_tag: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CharacterSet:
    """A set of characters for a specific story/episode (max 3)."""
    set_id: str
    story_id: str
    characters: List[Character]
    max_count: int = 3

    def __post_init__(self):
        if len(self.characters) > self.max_count:
            raise ValueError(f"CharacterSet cannot exceed {self.max_count} characters")


@dataclass
class ReferenceImage:
    """Reference image data for maintaining character consistency."""
    character_id: str
    image_url: str
    seed: str
    style_locked: bool = False


@dataclass
class StyleProfile:
    """Visual style profile for a story to ensure consistency."""
    story_id: str
    visual_style: str
    mood: str
    lighting: str
    color_palette: str
    cinematic_rules: str
