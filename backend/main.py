"""
AI Video Generation Platform - Main Entry Point
Запуск UVicorn сервера
"""
import uvicorn
from app import create_app
from core.config import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
