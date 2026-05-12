"""
Конфигурация приложения
Загрузка переменных окружения и настроек
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # AI Provider settings
    AI_PROVIDER: str = "openai"  # openai | yandex | other
    AI_MODEL: str = "gpt-4"
    API_KEY: str = ""
    YANDEX_FOLDER_ID: str | None = None
    
    # TTS settings
    TTS_PROVIDER: str = "openai"
    
    # Colab Render settings
    COLAB_URL: str = "http://localhost:8080"
    
    # Output settings
    ORIENTATION: str = "vertical"  # vertical | horizontal | square
    RESOLUTION: str = "720p"  # 240p | 360p | 480p | 720p | 1080p
    
    # Subtitles
    SUBTITLES_ENABLED: bool = True
    
    # Storage paths
    STORAGE_PATH: str = "./storage"
    PROMPTS_PATH: str = "./storage/prompts"
    OUTPUTS_PATH: str = "./storage/outputs"
    TEMP_PATH: str = "./storage/temp"
    LOGS_PATH: str = "./storage/logs"
    CACHE_PATH: str = "./storage/cache"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Создание директорий при импорте
import os
os.makedirs(settings.STORAGE_PATH, exist_ok=True)
os.makedirs(settings.PROMPTS_PATH, exist_ok=True)
os.makedirs(settings.OUTPUTS_PATH, exist_ok=True)
os.makedirs(settings.TEMP_PATH, exist_ok=True)
os.makedirs(settings.LOGS_PATH, exist_ok=True)
os.makedirs(settings.CACHE_PATH, exist_ok=True)
