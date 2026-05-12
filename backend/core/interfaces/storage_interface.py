"""
Storage interface - abstract base class for storage implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..models import Project, Job, StageRun


class StorageInterface(ABC):
    """
    Абстрактный интерфейс для хранилища данных.
    
    Core система НЕ определяет storage implementation.
    Реализация предоставляется извне через dependency injection.
    """
    
    @abstractmethod
    def save_project(self, project: Project) -> None:
        """Сохраняет проект в хранилище."""
        pass
    
    @abstractmethod
    def get_project(self, project_id: str) -> Project:
        """
        Получает проект по ID.
        
        RAISES:
            ValueError если проект не найден
        """
        pass
    
    @abstractmethod
    def save_job(self, job: Job) -> None:
        """Сохраняет job в хранилище."""
        pass
    
    @abstractmethod
    def get_job(self, job_id: str) -> Job:
        """
        Получает job по ID.
        
        RAISES:
            ValueError если job не найден
        """
        pass
    
    @abstractmethod
    def save_stage_run(self, stage_run: StageRun) -> None:
        """Сохраняет stage run в хранилище."""
        pass
    
    @abstractmethod
    def get_stage_runs(self, job_id: str) -> List[StageRun]:
        """
        Получает все stage runs для job.
        
        RETURNS:
            Список StageRun объектов
        """
        pass
