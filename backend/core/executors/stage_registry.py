"""
Stage registry for managing stage implementations.
"""

from typing import Dict

from ..interfaces import StageInterface


# Static list of all pipeline stages
STAGES = [
    "story_generation",
    "character_extraction",
    "story_adaptation",
    "storyboard_generation",
    "tts_generation",
    "subtitle_generation",
    "character_render",
    "scene_image_generation",
    "manifest_generation",
    "video_render",
    "metadata_generation"
]


def validate_stage_name(stage_name: str) -> bool:
    """
    Проверяет, является ли имя этапа валидным.
    
    Args:
        stage_name: Имя этапа для проверки
        
    Returns:
        True если этап валидный, False иначе
    """
    return stage_name in STAGES


class StageRegistry:
    """
    Регистр всех stage-реализаций.
    
    Core НЕ импортирует stages напрямую.
    Реализации регистрируются извне при инициализации системы.
    """
    
    def __init__(self):
        """Инициализирует пустой регистр."""
        self._stages: Dict[str, StageInterface] = {}
    
    def register(self, stage: StageInterface) -> None:
        """
        Регистрирует stage implementation.
        
        Args:
            stage: StageInterface implementation
            
        Вызывается при инициализации системы из другого модуля.
        """
        if not isinstance(stage, StageInterface):
            raise TypeError("Stage must implement StageInterface")
        
        if not validate_stage_name(stage.stage_name):
            raise ValueError(f"Invalid stage name '{stage.stage_name}'")
        
        self._stages[stage.stage_name] = stage
    
    def get_stage(self, stage_name: str) -> StageInterface:
        """
        Получает stage implementation по имени.
        
        Args:
            stage_name: Имя этапа
            
        Returns:
            StageInterface implementation
            
        Raises:
            KeyError если stage не зарегистрирован
        """
        if stage_name not in self._stages:
            raise KeyError(f"Stage '{stage_name}' not registered")
        return self._stages[stage_name]
    
    def is_registered(self, stage_name: str) -> bool:
        """
        Проверяет, зарегистрирован ли stage.
        
        Args:
            stage_name: Имя этапа
            
        Returns:
            True если зарегистрирован, False иначе
        """
        return stage_name in self._stages
    
    def get_all_stages(self) -> Dict[str, StageInterface]:
        """
        Возвращает все зарегистрированные stages.
        
        Returns:
            Dict mapping stage_name to StageInterface
        """
        return self._stages.copy()
