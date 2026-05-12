"""
Scene Builder
=============
Строит полную сцену из текста, персонажей и стиля.
"""

import uuid
from typing import List, Dict, Any, Optional

from .scene_schema import Scene
from .prompt_builder import PromptBuilder


# Импорты схем из других блоков (для типизации)
# from ..characters.character_schema import Character, StyleProfile


class SceneBuilder:
    """
    Строит объекты Scene из входных данных.
    """
    
    def __init__(self):
        self.prompt_builder = PromptBuilder()
    
    def build_scene(
        self,
        scene_text: str,
        characters: List[Dict[str, Any]],  # Character[] из блока 4
        style_profile: Dict[str, Any],  # StyleProfile из блока 4
        story_id: str = "",
        index: int = 0,
        mood: str = "",
        existing_scene: Optional[Scene] = None
    ) -> Scene:
        """
        Создает полную сцену с визуальным промптом.
        
        INPUT:
            scene_text: текст сцены (voiceover)
            characters: список персонажей для этой сцены
            style_profile: профиль стиля
            story_id: ID истории
            index: индекс сцены
            mood: настроение сцены
            existing_scene: существующая сцена для обновления
        
        OUTPUT:
            Scene с заполненными полями
        """
        # Если есть существующая сцена - обновляем её
        if existing_scene:
            scene = existing_scene
        else:
            scene = Scene(
                scene_id=str(uuid.uuid4()),
                story_id=story_id,
                index=index,
                voice_text=scene_text.strip(),
                visual_prompt="",
                characters=[],
                mood=mood or style_profile.get("mood", ""),
                style=style_profile.get("visual_style", ""),
                camera_motion="static",
                transition="cut",
                estimated_duration_sec=None,
                subtitle_text=scene_text.strip()
            )
        
        # Извлекаем ID персонажей
        character_ids = [ch.get("character_id", "") for ch in characters if ch.get("character_id")]
        scene.characters = character_ids
        
        # Генерируем визуальный промпт
        prompt_result = self.prompt_builder.build_visual_prompt(
            scene=scene,
            characters=characters
        )
        scene.visual_prompt = prompt_result["prompt"]
        
        return scene
    
    def update_scene_transition(
        self,
        scene: Scene,
        transition: str
    ) -> Scene:
        """
        Обновляет тип перехода для сцены.
        """
        valid_transitions = ["cut", "fade", "glitch", "blur"]
        if transition in valid_transitions:
            scene.transition = transition
        return scene
    
    def update_scene_motion(
        self,
        scene: Scene,
        camera_motion: str
    ) -> Scene:
        """
        Обновляет движение камеры для сцены.
        """
        valid_motions = ["static", "zoom_in", "zoom_out", "pan", "shake"]
        if camera_motion in valid_motions:
            scene.camera_motion = camera_motion
        return scene
