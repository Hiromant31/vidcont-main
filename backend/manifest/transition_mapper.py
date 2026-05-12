"""
Transition Mapper

Определяет типы переходов между сценами на основе контекста.
"""

from typing import List, Dict, Any, Optional
from .render_schema import TransitionMap, ManifestScene


class TransitionMapper:
    """
    Маппер переходов между сценами.
    
    Определяет тип перехода на основе:
    - напряжённости сцены
    - смены настроения
    - логической связи между сценами
    """
    
    # Типы переходов
    TRANSITION_CUT = "cut"
    TRANSITION_FADE = "fade"
    TRANSITION_GLITCH = "glitch"
    TRANSITION_BLUR = "blur"
    TRANSITION_ZOOM = "zoom"
    
    # Длительности переходов по умолчанию (сек)
    TRANSITION_DURATIONS = {
        TRANSITION_CUT: 0.0,
        TRANSITION_FADE: 0.5,
        TRANSITION_GLITCH: 0.3,
        TRANSITION_BLUR: 0.4,
        TRANSITION_ZOOM: 0.6,
    }
    
    def map_transitions(
        self,
        scenes: List[Dict[str, Any]]
    ) -> List[TransitionMap]:
        """
        Создать карту переходов для всех сцен.
        
        Args:
            scenes: Список сцен с метаданными (mood, intent, etc.)
            
        Returns:
            Список объектов TransitionMap
        """
        if len(scenes) < 2:
            return []
        
        transitions = []
        
        for i in range(len(scenes) - 1):
            current_scene = scenes[i]
            next_scene = scenes[i + 1]
            
            transition_type = self._determine_transition_type(
                current_scene,
                next_scene
            )
            
            transition = TransitionMap(
                from_scene_id=current_scene.get("scene_id", f"scene_{i}"),
                to_scene_id=next_scene.get("scene_id", f"scene_{i+1}"),
                type=transition_type,
                duration_sec=self.TRANSITION_DURATIONS.get(transition_type, 0.5)
            )
            
            transitions.append(transition)
        
        return transitions
    
    def _determine_transition_type(
        self,
        current_scene: Dict[str, Any],
        next_scene: Dict[str, Any]
    ) -> str:
        """
        Определить тип перехода между двумя сценами.
        
        Логика:
        - напряжённые сцены → glitch
        - спокойные → fade
        - резкие повороты → cut
        - смена настроения → blur
        """
        current_mood = current_scene.get("mood", "").lower()
        next_mood = next_scene.get("mood", "").lower()
        current_intent = current_scene.get("intent", "").lower()
        next_intent = next_scene.get("intent", "").lower()
        
        # Проверка на напряжённость/экшен
        tense_keywords = ["tense", "action", "dramatic", "intense", "conflict"]
        if any(kw in current_mood or kw in current_intent for kw in tense_keywords):
            return self.TRANSITION_GLITCH
        
        # Проверка на спокойствие
        calm_keywords = ["calm", "peaceful", "slow", "reflective", "emotional"]
        if all(kw in current_mood or kw in next_mood for kw in calm_keywords[:2]):
            return self.TRANSITION_FADE
        
        # Проверка на резкую смену настроения
        mood_change = self._detect_mood_change(current_mood, next_mood)
        if mood_change:
            return self.TRANSITION_BLUR
        
        # Резкий поворот сюжета
        plot_keywords = ["twist", "reveal", "shock", "surprise"]
        if any(kw in next_intent for kw in plot_keywords):
            return self.TRANSITION_CUT
        
        # По умолчанию - плавный переход
        return self.TRANSITION_FADE
    
    def _detect_mood_change(self, mood1: str, mood2: str) -> bool:
        """Обнаружить значительную смену настроения."""
        positive_keywords = ["happy", "joyful", "bright", "hopeful", "uplifting"]
        negative_keywords = ["sad", "dark", "gloomy", "depressing", "ominous"]
        
        mood1_positive = any(kw in mood1 for kw in positive_keywords)
        mood1_negative = any(kw in mood1 for kw in negative_keywords)
        mood2_positive = any(kw in mood2 for kw in positive_keywords)
        mood2_negative = any(kw in mood2 for kw in negative_keywords)
        
        # Смена с позитива на негатив или наоборот
        if (mood1_positive and mood2_negative) or (mood1_negative and mood2_positive):
            return True
        
        return False
    
    def get_transition_for_scene(
        self,
        scene_index: int,
        total_scenes: int,
        mood: str = "",
        intent: str = ""
    ) -> Dict[str, Any]:
        """
        Получить параметры перехода для конкретной сцены.
        
        Args:
            scene_index: Индекс сцены
            total_scenes: Общее количество сцен
            mood: Настроение сцены
            intent: Интент сцены
            
        Returns:
            Dict с типом и длительностью перехода
        """
        if scene_index >= total_scenes - 1:
            # Последняя сцена не имеет перехода
            return {
                "type": None,
                "duration_sec": 0.0
            }
        
        scene_data = {
            "scene_id": f"scene_{scene_index}",
            "mood": mood,
            "intent": intent
        }
        
        # Создаём фиктивную следующую сцену для определения типа перехода
        next_scene_data = {
            "scene_id": f"scene_{scene_index + 1}",
            "mood": "",
            "intent": ""
        }
        
        transition_type = self._determine_transition_type(scene_data, next_scene_data)
        
        return {
            "type": transition_type,
            "duration_sec": self.TRANSITION_DURATIONS.get(transition_type, 0.5)
        }
