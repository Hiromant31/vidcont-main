"""
Scene Splitter
==============
Разбивает voiceover script на логические сцены.
Каждая сцена = 1 смысловой блок.
"""

import uuid
from typing import List, Dict, Any

from .scene_schema import Scene, SceneSet


class SceneSplitter:
    """
    Разделяет скрипт озвучки на отдельные сцены.
    """
    
    def split_script_into_scenes(
        self,
        voiceover_script: str,
        target_scene_count: int
    ) -> SceneSet:
        """
        Разбивает скрипт на целевое количество сцен.
        
        INPUT:
            voiceover_script: полный текст озвучки
            target_scene_count: желаемое количество сцен
        
        OUTPUT:
            SceneSet с набором сцен
        """
        if not voiceover_script or not voiceover_script.strip():
            return SceneSet(story_id="", scenes=[], total_scenes=0)
        
        # Разбиваем текст на абзацы/предложения
        paragraphs = self._split_text_into_segments(voiceover_script)
        
        # Если сегментов меньше чем нужно сцен - используем их как есть
        # Если больше - объединяем или делим равномерно
        segments = self._distribute_segments(paragraphs, target_scene_count)
        
        scenes = []
        for idx, segment in enumerate(segments):
            scene = Scene(
                scene_id=str(uuid.uuid4()),
                story_id="",  # будет установлен позже
                index=idx,
                voice_text=segment.strip(),
                visual_prompt="",  # будет заполнен PromptBuilder
                characters=[],
                mood="",
                style="",
                camera_motion="static",
                transition="cut" if idx == 0 else "cut",
                estimated_duration_sec=None,  # будет оценен TimingEstimator
                subtitle_text=segment.strip()
            )
            scenes.append(scene)
        
        return SceneSet(
            story_id="",
            scenes=scenes,
            total_scenes=len(scenes)
        )
    
    def _split_text_into_segments(self, text: str) -> List[str]:
        """
        Разбивает текст на смысловые сегменты.
        Приоритет: абзацы > предложения.
        """
        # Сначала пробуем разбить по абзацам
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if len(paragraphs) >= 2:
            return paragraphs
        
        # Если абзацев мало, разбиваем по предложениям
        sentences = self._split_by_sentences(text)
        return sentences
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """
        Разбивает текст на предложения.
        """
        import re
        # Простая эвристика: разбиваем по . ! ?
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _distribute_segments(
        self,
        segments: List[str],
        target_count: int
    ) -> List[str]:
        """
        Распределяет сегменты по целевому количеству сцен.
        """
        if not segments:
            return []
        
        if len(segments) <= target_count:
            # Сегментов меньше или равно - возвращем как есть
            # (сцены будут короче, но это лучше чем искусственное деление)
            return segments
        
        # Сегментов больше чем нужно - объединяем соседние
        result = []
        segments_per_scene = len(segments) / target_count
        
        current_scene = ""
        count = 0
        
        for segment in segments:
            current_scene += (" " if current_scene else "") + segment
            count += 1
            
            if count >= segments_per_scene:
                result.append(current_scene)
                current_scene = ""
                count = 0
        
        # Добавляем остаток
        if current_scene:
            result.append(current_scene)
        
        # Убеждаемся что количество совпадает
        while len(result) < target_count and result:
            # Если сцен мало, делим самые длинные
            longest_idx = max(range(len(result)), key=lambda i: len(result[i]))
            longest = result[longest_idx]
            mid = len(longest) // 2
            
            # Находим ближайший пробел к середине
            space_pos = longest.rfind(' ', 0, mid)
            if space_pos == -1:
                space_pos = mid
            
            part1 = longest[:space_pos].strip()
            part2 = longest[space_pos:].strip()
            
            result[longest_idx] = part1
            result.insert(longest_idx + 1, part2)
        
        return result[:target_count] if len(result) > target_count else result
