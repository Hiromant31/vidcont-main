"""
Health check endpoints
"""
from fastapi import APIRouter
from typing import Dict, List

router = APIRouter()

@router.get("/")
async def health_check():
    """Базовая проверка здоровья сервиса"""
    return {"status": "healthy", "service": "ai-video-platform"}

@router.get("/colab")
async def colab_health():
    """Проверка подключения к Colab серверу"""
    # TODO: Реальная проверка подключения к Colab
    return {"status": "unknown", "message": "Colab health check not implemented"}

@router.get("/pipeline")
async def pipeline_health():
    """Проверка состояния пайплайна"""
    return {
        "status": "ready",
        "stages_available": [
            "story_generation",
            "character_extraction",
            "scene_generation",
            "tts_generation",
            "manifest_build",
            "render"
        ]
    }
