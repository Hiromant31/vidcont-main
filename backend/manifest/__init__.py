"""
MANIFEST + RENDER PREP SYSTEM

Этот блок отвечает за:
- сбор всех данных в единый render manifest
- подготовку таймингов для ffmpeg
- привязку сцен → аудио → визуал → субтитры
- управление переходами и монтажом
- формирование задания для Colab-рендера
"""

from .render_schema import (
    Manifest,
    ManifestScene,
    TransitionMap,
    RenderPack,
)
from .manifest_builder import ManifestBuilder
from .timeline_calculator import TimelineCalculator
from .transition_mapper import TransitionMapper
from .ffmpeg_instruction_builder import FFmpegInstructionBuilder
from .export_packager import ExportPackager

__all__ = [
    "Manifest",
    "ManifestScene",
    "TransitionMap",
    "RenderPack",
    "ManifestBuilder",
    "TimelineCalculator",
    "TransitionMapper",
    "FFmpegInstructionBuilder",
    "ExportPackager",
]
