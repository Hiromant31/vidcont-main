"""
Prompt Builder for Scenes
=========================
Строит визуальные промпты для сцен, комбинируя персонажей, стиль и окружение.
"""

from typing import List, Dict, Any

from .scene_schema import Scene, ScenePromptPack


class PromptBuilder:
    """
    Генерирует финальные визуальные промпты для сцен.
    """
    
    def build_visual_prompt(
        self,
        scene: Scene,
        characters: List[Dict[str, Any]]  # Character[] из блока 4
    ) -> Dict[str, str]:
        """
        Создает полный визуальный промпт для сцены.
        
        INPUT:
            scene: объект сцены
            characters: список персонажей с их visual_prompt
        
        OUTPUT:
            {"prompt": "полный промпт"}
        """
        # Базовый промпт из описания сцены
        base_prompt = self._create_base_prompt(scene)
        
        # Промпты персонажей
        character_prompts = []
        for char in characters:
            if char.get("visual_prompt"):
                character_prompts.append(char["visual_prompt"])
        
        # Стилевой промпт
        style_prompt = self._create_style_prompt(scene)
        
        # Комбинируем в финальный промпт
        final_prompt = self._combine_prompts(
            base_prompt=base_prompt,
            character_prompts=character_prompts,
            style_prompt=style_prompt,
            motion=scene.camera_motion
        )
        
        return {
            "prompt": final_prompt
        }
    
    def build_prompt_pack(
        self,
        scene: Scene,
        characters: List[Dict[str, Any]]
    ) -> ScenePromptPack:
        """
        Создает полный пакет промптов для сцены.
        """
        base_prompt = self._create_base_prompt(scene)
        
        character_prompts = [
            ch.get("visual_prompt", "") 
            for ch in characters 
            if ch.get("visual_prompt")
        ]
        
        style_prompt = self._create_style_prompt(scene)
        
        final_result = self.build_visual_prompt(scene, characters)
        
        return ScenePromptPack(
            scene_id=scene.scene_id,
            base_prompt=base_prompt,
            character_prompts=character_prompts,
            style_prompt=style_prompt,
            final_prompt=final_result["prompt"]
        )
    
    def _create_base_prompt(self, scene: Scene) -> str:
        """
        Создает базовый промпт на основе текста сцены.
        """
        # Извлекаем ключевые элементы из voice_text
        voice_text = scene.voice_text
        
        # Формируем описание сцены
        base = (
            f"Scene depicting: {voice_text}. "
            f"Mood: {scene.mood or 'neutral'}. "
            f"Style: {scene.style or 'cinematic'}."
        )
        
        return base
    
    def _create_style_prompt(self, scene: Scene) -> str:
        """
        Создает стилевой промпт.
        """
        style_elements = []
        
        if scene.style:
            style_elements.append(f"Visual style: {scene.style}")
        
        if scene.mood:
            style_elements.append(f"Atmosphere: {scene.mood}")
        
        # Добавляем кинематографические параметры по умолчанию
        style_elements.append("high quality, detailed, professional composition")
        
        return ", ".join(style_elements)
    
    def _combine_prompts(
        self,
        base_prompt: str,
        character_prompts: List[str],
        style_prompt: str,
        motion: str
    ) -> str:
        """
        Комбинирует все части в единый промпт.
        """
        parts = []
        
        # Базовое описание
        parts.append(base_prompt)
        
        # Персонажи (если есть)
        if character_prompts:
            chars_text = "Characters: " + "; ".join(character_prompts)
            parts.append(chars_text)
        
        # Стиль
        parts.append(style_prompt)
        
        # Движение камеры
        motion_descriptions = {
            "static": "Static camera shot",
            "zoom_in": "Slow zoom in",
            "zoom_out": "Slow zoom out",
            "pan": "Camera panning motion",
            "shake": "Slight camera shake for tension"
        }
        motion_text = motion_descriptions.get(motion, "Static camera shot")
        parts.append(f"Camera: {motion_text}")
        
        return " | ".join(parts)
