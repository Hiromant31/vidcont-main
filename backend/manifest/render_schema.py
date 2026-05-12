"""
Render Schema Definitions

Содержит все data-схемы для манифеста рендеринга.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class SubtitleRange:
    """Диапазон субтитров для сцены."""
    start_index: int
    end_index: int


@dataclass
class ManifestScene:
    """
    Сцена в манифесте рендеринга.
    
    Атрибуты:
        scene_id: Уникальный идентификатор сцены
        start_time_sec: Время начала сцены в видео (сек)
        end_time_sec: Время конца сцены в видео (сек)
        duration_sec: Длительность сцены (сек)
        image_path: Путь к изображению сцены
        audio_path: Путь к аудио сцены
        visual_prompt: Визуальный промпт для генерации
        camera_motion: Движение камеры
        transition: Тип перехода к следующей сцене
        subtitle_range: Диапазон субтитров для этой сцены
    """
    scene_id: str
    start_time_sec: float
    end_time_sec: float
    duration_sec: float
    image_path: str
    audio_path: str
    visual_prompt: str
    camera_motion: str
    transition: str
    subtitle_range: SubtitleRange


@dataclass
class TransitionMap:
    """
    Карта переходов между сценами.
    
    Атрибуты:
        from_scene_id: ID исходной сцены
        to_scene_id: ID целевой сцены
        type: Тип перехода (cut, fade, zoom, glitch, blur)
        duration_sec: Длительность перехода (сек)
    """
    from_scene_id: str
    to_scene_id: str
    type: str
    duration_sec: float


@dataclass
class SubtitleEntry:
    """
    Entry субтитра.
    
    Атрибуты:
        index: Индекс субтитра
        start_time_sec: Время начала (сек)
        end_time_sec: Время конца (сек)
        text: Текст субтитра
    """
    index: int
    start_time_sec: float
    end_time_sec: float
    text: str


@dataclass
class Manifest:
    """
    Главный манифест рендеринга.
    
    Это "контракт между AI и ffmpeg".
    
    Атрибуты:
        job_id: Уникальный идентификатор задания
        orientation: Ориентация видео (vertical, horizontal, square)
        resolution: Разрешение видео (240p, 360p, 480p, 720p, 1080p)
        total_duration_sec: Общая длительность видео (сек)
        scenes: Список сцен
        subtitles: Список субтитров
        audio_tracks: Список путей к аудио трекам
        background_music: Путь к фоновой музыке (опционально)
        transitions: Карта переходов
    """
    job_id: str
    orientation: str  # "vertical" | "horizontal" | "square"
    resolution: str  # "240p" | "360p" | "480p" | "720p" | "1080p"
    total_duration_sec: float
    scenes: List[ManifestScene]
    subtitles: List[SubtitleEntry]
    audio_tracks: List[str]
    background_music: Optional[str] = None
    transitions: List[TransitionMap] = field(default_factory=list)


@dataclass
class RenderPack:
    """
    Финальный пакет для рендеринга.
    
    Атрибуты:
        manifest: Объект манифеста
        ffmpeg_script: Скрипт команд для ffmpeg
        assets_list: Список всех необходимых ассетов
        subtitles_file: Путь к файлу субтитров
    """
    manifest: Manifest
    ffmpeg_script: str
    assets_list: List[str]
    subtitles_file: str
