"""
Timing Estimator
================
Оценивает предполагаемую длительность сцены по тексту.
ВАЖНО: Это только оценка. Финальная длительность берется из TTS (блок 6).
"""

from typing import Dict, Any

from .scene_schema import Scene


class TimingEstimator:
    """
    Оценивает длительность сцены на основе текста озвучки.
    """
    
    # Средняя скорость речи (слов в минуту)
    # Русский: ~120-150 слов/мин, Английский: ~130-160 слов/мин
    AVG_WORDS_PER_MINUTE = {
        "ru": 130,
        "en": 140,
        "default": 135
    }
    
    # Минимальная и максимальная длительность сцены (сек)
    MIN_SCENE_DURATION = 2
    MAX_SCENE_DURATION = 15
    
    def estimate_duration(self, scene_text: str) -> Dict[str, int]:
        """
        Оценивает длительность сцены по тексту.
        
        INPUT:
            scene_text: текст озвучки сцены
        
        OUTPUT:
            {"estimated_duration_sec": int}
        """
        if not scene_text or not scene_text.strip():
            return {"estimated_duration_sec": self.MIN_SCENE_DURATION}
        
        # Определяем язык (простая эвристика)
        language = self._detect_language(scene_text)
        
        # Считаем количество слов
        word_count = self._count_words(scene_text)
        
        # Вычисляем длительность
        wpm = self.AVG_WORDS_PER_MINUTE.get(
            language, 
            self.AVG_WORDS_PER_MINUTE["default"]
        )
        
        # duration = (word_count / wpm) * 60 секунд
        estimated_sec = int((word_count / wpm) * 60)
        
        # Ограничиваем мин/макс
        estimated_sec = max(self.MIN_SCENE_DURATION, estimated_sec)
        estimated_sec = min(self.MAX_SCENE_DURATION, estimated_sec)
        
        return {"estimated_duration_sec": estimated_sec}
    
    def estimate_scene(self, scene: Scene) -> Dict[str, int]:
        """
        Оценивает длительность для объекта Scene.
        """
        return self.estimate_duration(scene.voice_text)
    
    def _detect_language(self, text: str) -> str:
        """
        Простая детекция языка.
        """
        # Кириллические символы
        cyrillic_chars = sum(1 for c in text if 'а' <= c.lower() <= 'я' or c == 'ё')
        latin_chars = sum(1 for c in text if 'a' <= c.lower() <= 'z')
        
        if cyrillic_chars > latin_chars:
            return "ru"
        elif latin_chars > 0:
            return "en"
        
        return "default"
    
    def _count_words(self, text: str) -> int:
        """
        Подсчитывает количество слов в тексте.
        """
        # Разбиваем по пробелам и фильтраем пустые
        words = [w for w in text.split() if w.strip()]
        return len(words)
    
    def estimate_batch(self, scenes: list) -> Dict[str, int]:
        """
        Оценивает общую длительность набора сцен.
        
        INPUT:
            scenes: список Scene или строк
        
        OUTPUT:
            {"estimated_duration_sec": total_seconds}
        """
        total = 0
        
        for scene in scenes:
            if isinstance(scene, Scene):
                result = self.estimate_scene(scene)
            else:
                result = self.estimate_duration(str(scene))
            
            total += result["estimated_duration_sec"]
        
        return {"estimated_duration_sec": total}
    
    def adjust_for_pacing(
        self,
        estimated_sec: int,
        pacing: str = "normal"
    ) -> int:
        """
        Корректирует длительность в зависимости от темпа.
        
        pacing: "slow" | "normal" | "fast"
        """
        multipliers = {
            "slow": 1.3,
            "normal": 1.0,
            "fast": 0.8
        }
        
        multiplier = multipliers.get(pacing, 1.0)
        adjusted = int(estimated_sec * multiplier)
        
        return max(self.MIN_SCENE_DURATION, min(self.MAX_SCENE_DURATION, adjusted))
