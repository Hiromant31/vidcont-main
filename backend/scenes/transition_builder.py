"""
Transition Builder
==================
Определяет тип перехода между сценами.
"""

from typing import Dict, Any, Optional

from .scene_schema import Scene


class TransitionBuilder:
    """
    Генерирует переходы между сценами на основе их контента и настроения.
    """
    
    # Переходы по умолчанию для разных ситуаций
    DEFAULT_TRANSITIONS = {
        "same_mood": "cut",
        "mood_change": "fade",
        "time_jump": "fade",
        "location_change": "cut",
        "tense_sequence": "glitch",
        "dream_sequence": "blur",
    }
    
    def generate_transition(
        self,
        previous_scene: Optional[Scene],
        current_scene: Scene
    ) -> Dict[str, str]:
        """
        Определяет оптимальный переход между сценами.
        
        INPUT:
            previous_scene: предыдущая сцена (None для первой)
            current_scene: текущая сцена
        
        OUTPUT:
            {"transition": "cut | fade | glitch | blur"}
        """
        # Первая сцена - всегда cut (или можно fade in)
        if previous_scene is None:
            return {"transition": "cut"}
        
        # Анализируем изменения между сценами
        mood_changed = self._detect_mood_change(previous_scene, current_scene)
        location_changed = self._detect_location_change(previous_scene, current_scene)
        time_changed = self._detect_time_change(previous_scene, current_scene)
        
        # Определяем тип перехода
        transition = self._determine_transition(
            mood_changed=mood_changed,
            location_changed=location_changed,
            time_changed=time_changed,
            current_mood=current_scene.mood
        )
        
        return {"transition": transition}
    
    def _detect_mood_change(self, prev: Scene, curr: Scene) -> bool:
        """
        Проверяет, изменилось ли настроение между сценами.
        """
        if not prev.mood or not curr.mood:
            return False
        
        return prev.mood.lower() != curr.mood.lower()
    
    def _detect_location_change(self, prev: Scene, curr: Scene) -> bool:
        """
        Проверяет, изменилось ли место действия.
        Эвристика: ищем ключевые слова мест в визуальном промпте.
        """
        # Простая эвристика: если промпты сильно различаются - возможно смена локации
        if not prev.visual_prompt or not curr.visual_prompt:
            return False
        
        # Можно улучшить NLP-анализом
        return prev.visual_prompt != curr.visual_prompt
    
    def _detect_time_change(self, prev: Scene, curr: Scene) -> bool:
        """
        Проверяет, изменилось ли время действия.
        Ищем ключевые слова времени в тексте.
        """
        time_keywords = [
            "утро", "день", "вечер", "ночь",
            "morning", "day", "evening", "night",
            "спустя", "later", "then", "после",
            "годы спустя", "years later"
        ]
        
        text_lower = curr.voice_text.lower()
        
        for keyword in time_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    def _determine_transition(
        self,
        mood_changed: bool,
        location_changed: bool,
        time_changed: bool,
        current_mood: str
    ) -> str:
        """
        Выбирает тип перехода на основе изменений.
        """
        # Приоритеты переходов
        
        # 1. Изменение времени - fade
        if time_changed:
            return "fade"
        
        # 2. Напряженное настроение - glitch
        if current_mood and any(word in current_mood.lower() for word in ["tense", "action", "horror"]):
            return "glitch"
        
        # 3. Смена настроения - fade
        if mood_changed:
            return "fade"
        
        # 4. Dreamy/mysterious - blur
        if current_mood and any(word in current_mood.lower() for word in ["dream", "mysterious", "memory"]):
            return "blur"
        
        # 5. По умолчанию - cut
        return "cut"
    
    def suggest_transition_variants(
        self,
        previous_scene: Optional[Scene],
        current_scene: Scene
    ) -> list:
        """
        Предлагает несколько вариантов перехода.
        """
        primary = self.generate_transition(previous_scene, current_scene)
        variants = [primary["transition"]]
        
        # Добавляем альтернативы
        all_transitions = ["cut", "fade", "glitch", "blur"]
        for t in all_transitions:
            if t not in variants:
                variants.append(t)
        
        return variants[:3]  # Возвращаем максимум 3 варианта
