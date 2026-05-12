"""
Scene System Module
===================
Блок 5: SCENE SYSTEM
Превращает сценарий в сцены для видео-производства.
"""

from .scene_schema import Scene, SceneSet, ScenePromptPack
from .scene_splitter import SceneSplitter
from .scene_builder import SceneBuilder
from .prompt_builder import PromptBuilder
from .motion_generator import MotionGenerator
from .transition_builder import TransitionBuilder
from .timing_estimator import TimingEstimator

__all__ = [
    # Schemas
    "Scene",
    "SceneSet",
    "ScenePromptPack",
    
    # Core components
    "SceneSplitter",
    "SceneBuilder",
    "PromptBuilder",
    "MotionGenerator",
    "TransitionBuilder",
    "TimingEstimator",
]
