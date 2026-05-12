"""
Manifest Builder

Собирает все данные в единый Manifest для рендеринга.
"""

from typing import List, Dict, Any, Optional
from .render_schema import (
    Manifest,
    ManifestScene,
    TransitionMap,
    SubtitleEntry,
    SubtitleRange,
)
from .timeline_calculator import TimelineCalculator
from .transition_mapper import TransitionMapper


class ManifestBuilder:
    """
    Строитель манифеста рендеринга.
    
    Собирает данные из всех предыдущих блоков:
    - Scenes (визуал, motion)
    - SceneAudio (тайминги, аудио)
    - Subtitles (субтитры)
    """
    
    def build_manifest(
        self,
        scenes: List[Dict[str, Any]],
        scene_audio: List[Dict[str, Any]],
        subtitles: List[Dict[str, Any]],
        orientation: str = "vertical",
        resolution: str = "720p",
        job_id: Optional[str] = None,
        background_music: Optional[str] = None
    ) -> Manifest:
        """
        Построить полный манифест рендеринга.
        
        Args:
            scenes: Список сцен из Scene System
            scene_audio: Список аудио-данных из TTS Sync System
            subtitles: Список субтитров из Subtitle Generator
            orientation: Ориентация видео
            resolution: Разрешение видео
            job_id: Уникальный ID задания
            background_music: Путь к фоновой музыке
            
        Returns:
            Объект Manifest
        """
        if not job_id:
            import uuid
            job_id = str(uuid.uuid4())
        
        # Рассчитываем тайминги
        timeline_calc = TimelineCalculator()
        timeline_result = timeline_calc.calculate_timeline(scene_audio)
        timed_scenes = timeline_result["timed_scenes"]
        total_duration = timeline_result["total_duration"]
        
        # Определяем переходы
        transition_mapper = TransitionMapper()
        transitions = transition_mapper.map_transitions(scenes)
        
        # Сопоставляем субтитры со сценами
        subtitle_ranges = self._map_subtitles_to_scenes(
            timed_scenes,
            subtitles
        )
        
        # Создаём ManifestScene объекты
        manifest_scenes = []
        for i, timed_scene in enumerate(timed_scenes):
            scene_data = scenes[i] if i < len(scenes) else {}
            
            subtitle_range = subtitle_ranges.get(
                timed_scene.scene_id,
                SubtitleRange(start_index=0, end_index=0)
            )
            
            manifest_scene = ManifestScene(
                scene_id=timed_scene.scene_id,
                start_time_sec=timed_scene.start_time_sec,
                end_time_sec=timed_scene.end_time_sec,
                duration_sec=timed_scene.duration_sec,
                image_path=timed_scene.image_path or scene_data.get("image_path", ""),
                audio_path=timed_scene.audio_path,
                visual_prompt=timed_scene.visual_prompt or scene_data.get("visual_prompt", ""),
                camera_motion=timed_scene.camera_motion or scene_data.get("camera_motion", "static"),
                transition=timed_scene.transition or scene_data.get("transition", "cut"),
                subtitle_range=subtitle_range
            )
            manifest_scenes.append(manifest_scene)
        
        # Создаём объекты SubtitleEntry
        subtitle_entries = [
            SubtitleEntry(
                index=sub.get("index", i),
                start_time_sec=sub.get("start_time_sec", 0.0),
                end_time_sec=sub.get("end_time_sec", 0.0),
                text=sub.get("text", "")
            )
            for i, sub in enumerate(subtitles)
        ]
        
        # Собираем аудио треки
        audio_tracks = [sa.get("audio_segment_path", "") for sa in scene_audio]
        
        # Создаём финальный манифест
        manifest = Manifest(
            job_id=job_id,
            orientation=orientation,
            resolution=resolution,
            total_duration_sec=total_duration,
            scenes=manifest_scenes,
            subtitles=subtitle_entries,
            audio_tracks=audio_tracks,
            background_music=background_music,
            transitions=transitions
        )
        
        return manifest
    
    def _map_subtitles_to_scenes(
        self,
        timed_scenes: List[Any],
        subtitles: List[Dict[str, Any]]
    ) -> Dict[str, SubtitleRange]:
        """
        Сопоставить субтитры со сценами.
        
        Args:
            timed_scenes: Список сцен с таймингами
            subtitles: Список субтитров
            
        Returns:
            Dict mapping scene_id -> SubtitleRange
        """
        result = {}
        
        for scene in timed_scenes:
            scene_start = scene.start_time_sec
            scene_end = scene.end_time_sec
            
            # Находим субтитры, попадающие в диапазон сцены
            start_index = None
            end_index = None
            
            for i, sub in enumerate(subtitles):
                sub_start = sub.get("start_time_sec", 0.0)
                sub_end = sub.get("end_time_sec", 0.0)
                
                # Проверяем пересечение
                if sub_start < scene_end and sub_end > scene_start:
                    if start_index is None:
                        start_index = i
                    end_index = i
            
            if start_index is not None and end_index is not None:
                result[scene.scene_id] = SubtitleRange(
                    start_index=start_index,
                    end_index=end_index
                )
            else:
                result[scene.scene_id] = SubtitleRange(
                    start_index=0,
                    end_index=0
                )
        
        return result
    
    def create_empty_manifest(self, job_id: str) -> Manifest:
        """
        Создать пустой манифест для инициализации.
        
        Args:
            job_id: Уникальный ID задания
            
        Returns:
            Пустой Manifest
        """
        return Manifest(
            job_id=job_id,
            orientation="vertical",
            resolution="720p",
            total_duration_sec=0.0,
            scenes=[],
            subtitles=[],
            audio_tracks=[],
            background_music=None,
            transitions=[]
        )
