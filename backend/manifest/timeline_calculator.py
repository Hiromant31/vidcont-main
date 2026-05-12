"""
Timeline Calculator

Вычисляет точные тайминги сцен на основе аудио.
scene duration = audio duration + gap между сценами
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TimedScene:
    """Сцена с рассчитанными таймингами."""
    scene_id: str
    start_time_sec: float
    end_time_sec: float
    duration_sec: float
    image_path: str
    audio_path: str
    visual_prompt: str
    camera_motion: str
    transition: str


class TimelineCalculator:
    """
    Калькулятор временной шкалы видео.
    
    Рассчитывает start_time и end_time для каждой сцены
    на основе длительности аудио.
    """
    
    DEFAULT_GAP_SEC = 0.5  # Пауза между сценами по умолчанию
    
    def calculate_timeline(
        self,
        scene_audio: List[Dict[str, Any]],
        gap_between_scenes: float = DEFAULT_GAP_SEC
    ) -> Dict[str, Any]:
        """
        Рассчитать тайминги для всех сцен.
        
        Args:
            scene_audio: Список объектов SceneAudio с данными о длительности
            gap_between_scenes: Пауза между сценами в секундах
            
        Returns:
            Dict с timed_scenes и total_duration
        """
        if not scene_audio:
            return {
                "timed_scenes": [],
                "total_duration": 0.0
            }
        
        timed_scenes = []
        current_time = 0.0
        
        for i, audio_data in enumerate(scene_audio):
            # Длительность аудио сцены
            audio_duration = audio_data.get("duration_sec", 0.0)
            
            # Общая длительность сцены = аудио + gap (если это не последняя сцена)
            is_last_scene = (i == len(scene_audio) - 1)
            scene_duration = audio_duration if is_last_scene else audio_duration + gap_between_scenes
            
            start_time = current_time
            end_time = start_time + scene_duration
            
            timed_scene = TimedScene(
                scene_id=audio_data.get("scene_id", f"scene_{i}"),
                start_time_sec=start_time,
                end_time_sec=end_time,
                duration_sec=scene_duration,
                image_path=audio_data.get("image_path", ""),
                audio_path=audio_data.get("audio_segment_path", ""),
                visual_prompt=audio_data.get("visual_prompt", ""),
                camera_motion=audio_data.get("camera_motion", "static"),
                transition=audio_data.get("transition", "cut")
            )
            
            timed_scenes.append(timed_scene)
            current_time = end_time
        
        total_duration = current_time
        
        return {
            "timed_scenes": timed_scenes,
            "total_duration": total_duration
        }
    
    def calculate_scene_timing(
        self,
        audio_duration: float,
        start_time: float,
        is_last: bool = False,
        gap: float = DEFAULT_GAP_SEC
    ) -> Dict[str, float]:
        """
        Рассчитать тайминг для одной сцены.
        
        Args:
            audio_duration: Длительность аудио сцены
            start_time: Время начала сцены
            is_last: Является ли сцена последней
            gap: Пауза после сцены
            
        Returns:
            Dict со start_time, end_time, duration
        """
        duration = audio_duration if is_last else audio_duration + gap
        end_time = start_time + duration
        
        return {
            "start_time_sec": start_time,
            "end_time_sec": end_time,
            "duration_sec": duration
        }
