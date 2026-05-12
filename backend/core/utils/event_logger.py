"""
Event logger for logging system events.
"""

import json
import logging
from datetime import datetime
from typing import Optional


class EventLogger:
    """
    Логгер событий системы.
    
    Логирует все значимые события в pipeline execution.
    """
    
    # Event types
    EVENT_TYPES = {
        # Stage events
        "stage_started",
        "stage_completed",
        "stage_failed",
        "stage_retrying",
        
        # Job events
        "job_started",
        "job_completed",
        "job_failed",
        
        # Retry events
        "retry_triggered"
    }
    
    def __init__(self, log_level: int = logging.INFO, log_file: Optional[str] = None):
        """
        Инициализирует EventLogger.
        
        Args:
            log_level: Уровень логирования
            log_file: Путь к файлу логов (None = console only)
        """
        self._logger = logging.getLogger("core_pipeline")
        self._logger.setLevel(log_level)
        
        # Clear existing handlers
        self._logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)
    
    def log_event(
        self,
        event_type: str,
        job_id: str,
        stage: Optional[str] = None,
        message: str = ""
    ) -> None:
        """
        Логирует событие в системе.
        
        Args:
            event_type: Тип события
            job_id: ID задачи
            stage: Имя этапа (если применимо)
            message: Дополнительное сообщение
            
        Event Types:
            - stage_started
            - stage_completed
            - stage_failed
            - stage_retrying
            - job_started
            - job_completed
            - job_failed
            - retry_triggered
            
        Output Format (JSON):
            {
                "event_type": str,
                "timestamp": datetime,
                "job_id": str,
                "stage": str | null,
                "message": str
            }
        """
        if event_type not in self.EVENT_TYPES:
            self._logger.warning(f"Unknown event type: {event_type}")
        
        # Build structured log entry
        log_entry = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "job_id": job_id,
            "stage": stage,
            "message": message
        }
        
        # Determine log level based on event type
        if "failed" in event_type:
            log_level = logging.ERROR
        elif "retry" in event_type:
            log_level = logging.WARNING
        else:
            log_level = logging.INFO
        
        # Log as JSON string for structured logging
        self._logger.log(log_level, json.dumps(log_entry))
    
    def log_stage_started(self, job_id: str, stage: str) -> None:
        """Удобный метод для логирования начала этапа."""
        self.log_event("stage_started", job_id, stage, f"Stage '{stage}' started")
    
    def log_stage_completed(self, job_id: str, stage: str) -> None:
        """Удобный метод для логирования завершения этапа."""
        self.log_event("stage_completed", job_id, stage, f"Stage '{stage}' completed")
    
    def log_stage_failed(self, job_id: str, stage: str, error: str) -> None:
        """Удобный метод для логирования ошибки этапа."""
        self.log_event("stage_failed", job_id, stage, f"Stage '{stage}' failed: {error}")
    
    def log_job_started(self, job_id: str) -> None:
        """Удобный метод для логирования начала job."""
        self.log_event("job_started", job_id, None, "Job started")
    
    def log_job_completed(self, job_id: str) -> None:
        """Удобный метод для логирования завершения job."""
        self.log_event("job_completed", job_id, None, "Job completed")
    
    def log_job_failed(self, job_id: str, error: str) -> None:
        """Удобный метод для логирования ошибки job."""
        self.log_event("job_failed", job_id, None, f"Job failed: {error}")
