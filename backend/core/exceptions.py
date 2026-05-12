"""
Кастомные исключения приложения
"""
from typing import Optional, List

class AppException(Exception):
    """Базовое исключение приложения"""
    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class PipelineException(AppException):
    """Исключение пайплайна"""
    def __init__(self, message: str, stage: Optional[str] = None):
        self.stage = stage
        super().__init__(message, code="PIPELINE_ERROR")

class JobException(AppException):
    """Исключение задачи"""
    def __init__(self, message: str, job_id: Optional[str] = None):
        self.job_id = job_id
        super().__init__(message, code="JOB_ERROR")

class RenderException(AppException):
    """Исключение рендера"""
    def __init__(self, message: str, render_job_id: Optional[str] = None):
        self.render_job_id = render_job_id
        super().__init__(message, code="RENDER_ERROR")

class AIProviderException(AppException):
    """Исключение AI провайдера"""
    def __init__(self, message: str, provider: Optional[str] = None):
        self.provider = provider
        super().__init__(message, code="AI_PROVIDER_ERROR")

class ValidationException(AppException):
    """Исключение валидации"""
    def __init__(self, message: str, fields: Optional[List[str]] = None):
        self.fields = fields or []
        super().__init__(message, code="VALIDATION_ERROR")

class StorageException(AppException):
    """Исключение хранилища"""
    def __init__(self, message: str, path: Optional[str] = None):
        self.path = path
        super().__init__(message, code="STORAGE_ERROR")
