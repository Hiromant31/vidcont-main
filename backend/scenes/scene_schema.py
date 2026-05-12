"""
Scene System Schemas
====================
Data models for scene management, visual prompts, and montage structure.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Scene:
    """
    Основная сущность сцены.
    Минимальная единица видео.
    """
    scene_id: str
    story_id: str
    index: int
    
    voice_text: str
    visual_prompt: str
    
    characters: List[str] = field(default_factory=list)
    
    mood: str = ""
    style: str = ""
    
    camera_motion: str = "static"  # static | zoom_in | zoom_out | pan | shake
    transition: str = "cut"  # cut | fade | glitch | blur
    
    estimated_duration_sec: Optional[int] = None
    
    subtitle_text: str = ""
    
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SceneSet:
    """
    Набор сцен для одной истории.
    """
    story_id: str
    scenes: List[Scene] = field(default_factory=list)
    total_scenes: int = 0
    
    def __post_init__(self):
        if self.total_scenes == 0:
            self.total_scenes = len(self.scenes)


@dataclass
class ScenePromptPack:
    """
    Пакет промптов для генерации сцены.
    """
    scene_id: str
    base_prompt: str
    character_prompts: List[str] = field(default_factory=list)
    style_prompt: str = ""
    final_prompt: str = ""
