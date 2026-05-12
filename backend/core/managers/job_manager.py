"""
Job manager for managing job lifecycle.
"""

from datetime import datetime
from typing import Optional

from ..models import Job
from ..interfaces import StorageInterface


class JobManager:
    """
    Менеджер для управления job'ами.
    
    Отвечает за создание, запуск и завершение job'ов.
    """
    
    def __init__(self, storage: StorageInterface):
        """
        Инициализирует JobManager.
        
        Args:
            storage: StorageInterface implementation для хранения данных
        """
        self._storage = storage
    
    def create_job(self, project_id: str) -> Job:
        """
        Создает новый job для проекта.
        
        Args:
            project_id: ID проекта
            
        Returns:
            Job с status="queued", current_stage=None
        """
        # Validate project exists
        from ..managers import ProjectManager
        project_manager = ProjectManager(self._storage)
        project_manager.get_project(project_id)  # Will raise if not found
        
        now = datetime.now()
        job = Job(
            job_id=self._generate_job_id(),
            project_id=project_id,
            status="queued",
            current_stage=None,
            created_at=now,
            started_at=None,
            finished_at=None,
            error=None
        )
        self._storage.save_job(job)
        return job
    
    def start_job(self, job_id: str) -> Job:
        """
        Запускает job.
        
        Args:
            job_id: ID job
            
        Returns:
            Обновленный Job объект
            
        Changes:
            status: "queued" -> "running"
            started_at: устанавливается datetime.now()
        """
        job = self._storage.get_job(job_id)
        job.status = "running"
        job.started_at = datetime.now()
        self._storage.save_job(job)
        return job
    
    def update_job_stage(self, job_id: str, stage_name: str) -> Job:
        """
        Обновляет текущий этап job.
        
        Args:
            job_id: ID job
            stage_name: Имя текущего этапа
            
        Returns:
            Обновленный Job объект
            
        Validates:
            stage_name из STAGES
        """
        from ..executors import validate_stage_name
        
        if not validate_stage_name(stage_name):
            raise ValueError(f"Invalid stage name '{stage_name}'")
        
        job = self._storage.get_job(job_id)
        job.current_stage = stage_name
        self._storage.save_job(job)
        return job
    
    def complete_job(self, job_id: str) -> Job:
        """
        Завершает job успешно.
        
        Args:
            job_id: ID job
            
        Returns:
            Обновленный Job объект
            
        Changes:
            status: "running" -> "completed"
            finished_at: устанавливается datetime.now()
        """
        job = self._storage.get_job(job_id)
        job.status = "completed"
        job.finished_at = datetime.now()
        self._storage.save_job(job)
        return job
    
    def fail_job(self, job_id: str, error: str) -> Job:
        """
        Помечает job как failed.
        
        Args:
            job_id: ID job
            error: Сообщение об ошибке
            
        Returns:
            Обновленный Job объект
            
        Changes:
            status: -> "failed"
            error: устанавливается сообщение
            finished_at: устанавливается datetime.now()
        """
        job = self._storage.get_job(job_id)
        job.status = "failed"
        job.error = error
        job.finished_at = datetime.now()
        self._storage.save_job(job)
        return job
    
    def get_job(self, job_id: str) -> Job:
        """
        Получает job по ID.
        
        Args:
            job_id: ID job
            
        Returns:
            Job объект
        """
        return self._storage.get_job(job_id)
    
    @staticmethod
    def _generate_job_id() -> str:
        """
        Генерирует уникальный ID для job.
        
        Returns:
            Уникальный строковый ID
        """
        import uuid
        return f"job_{uuid.uuid4().hex}"
