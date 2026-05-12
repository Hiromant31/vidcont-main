"""
Motion Generator
================
Генерирует тип движения камеры для сцены на основе её контента.
"""

from typing import Dict, Any, List

from .scene_schema import Scene


class MotionGenerator:
    """
    Определяет оптимальное движение камеры для сцены.
    """
    
    # Ключевые слова для определения типа движения
    MOTION_KEYWORDS = {
        "zoom_in": ["приближение", "крупный план", "focus", "close-up", "деталь", "вглядывается"],
        "zoom_out": ["отдаление", "общий план", "panorama", "wide shot", "вся сцена", "обзор"],
        "pan": ["панорама", "движение", "слева направо", "справа налево", "pan", "перемещение"],
        "shake": ["тряска", "нервно", "напряжение", "tension", "дрожь", "хаос", "битва"],
    }
    
    # Движения по умолчанию для разных настроений
    MOOD_MOTION_MAP = {
        "tense": "shake",
        "calm": "static",
        "dramatic": "zoom_in",
        "epic": "zoom_out",
        "romantic": "slow_pan",
        "action": "shake",
        "mysterious": "zoom_in",
    }
    
    def generate_camera_motion(self, scene: Scene) -> Dict[str, str]:
        """
        Генерирует тип движения камеры для сцены.
        
        INPUT:
            scene: объект сцены
        
        OUTPUT:
            {"camera_motion": "static | zoom_in | zoom_out | pan | shake"}
        """
        # Анализируем текст сцены
        text_lower = scene.voice_text.lower()
        subtitle_lower = scene.subtitle_text.lower()
        combined_text = f"{text_lower} {subtitle_lower}"
        
        # 1. Проверяем ключевые слова в тексте
        detected_motion = self._detect_motion_from_text(combined_text)
        if detected_motion:
            return {"camera_motion": detected_motion}
        
        # 2. Если не найдено - используем настроение
        mood_motion = self._get_motion_by_mood(scene.mood)
        if mood_motion:
            return {"camera_motion": mood_motion}
        
        # 3. По умолчанию - статичная камера
        return {"camera_motion": "static"}
    
    def _detect_motion_from_text(self, text: str) -> str:
        """
        Ищет ключевые слова движения в тексте.
        """
        motion_scores = {
            "zoom_in": 0,
            "zoom_out": 0,
            "pan": 0,
            "shake": 0,
        }
        
        for motion, keywords in self.MOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    motion_scores[motion] += 1
        
        # Возвращаем движение с наибольшим количеством совпадений
        max_score = max(motion_scores.values())
        if max_score > 0:
            for motion, score in motion_scores.items():
                if score == max_score:
                    return motion
        
        return ""
    
    def _get_motion_by_mood(self, mood: str) -> str:
        """
        Возвращает рекомендуемое движение по настроению.
        """
        mood_lower = mood.lower()
        
        # Прямое совпадение
        if mood_lower in self.MOOD_MOTION_MAP:
            return self.MOOD_MOTION_MAP[mood_lower]
        
        # Частичное совпадение
        for mood_key, motion in self.MOOD_MOTION_MAP.items():
            if mood_key in mood_lower or mood_lower in mood_key:
                return motion
        
        return ""
    
    def suggest_motion_variants(self, scene: Scene) -> List[str]:
        """
        Предлагает несколько вариантов движения для сцены.
        """
        variants = []
        
        # Основное движение
        primary = self.generate_camera_motion(scene)
        variants.append(primary["camera_motion"])
        
        # Альтернативы на основе настроения
        mood_alternatives = {
            "shake": ["static"],
            "static": ["zoom_in", "pan"],
            "zoom_in": ["zoom_out", "static"],
            "zoom_out": ["pan", "static"],
            "pan": ["static", "zoom_in"],
        }
        
        primary_motion = primary["camera_motion"]
        if primary_motion in mood_alternatives:
            variants.extend(mood_alternatives[primary_motion])
        
        return variants
