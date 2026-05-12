"""
Project manager for managing project lifecycle.
"""

from datetime import datetime
from typing import Optional

from ..models import Project
from ..interfaces import StorageInterface


class ProjectManager:
    """
    Менеджер для управления проектами.
    
    Отвечает за создание, получение и обновление проектов.
    """
    
    def __init__(self, storage: StorageInterface):
        """
        Инициализирует ProjectManager.
        
        Args:
            storage: StorageInterface implementation для хранения данных
        """
        self._storage = storage
    
    def create_project(self, name: str, settings_id: str) -> Project:
        """
        Создает новый проект.
        
        Args:
            name: Имя проекта
            settings_id: ID настроек из settings блока
            
        Returns:
            Project с status="created"
        """
        now = datetime.now()
        project = Project(
            project_id=self._generate_project_id(),
            name=name,
            status="created",
            settings_id=settings_id,
            active_job_id=None,
            created_at=now,
            updated_at=now
        )
        self._storage.save_project(project)
        return project
    
    def get_project(self, project_id: str) -> Project:
        """
        Получает проект по ID.
        
        Args:
            project_id: ID проекта
            
        Returns:
            Project объект
            
        Raises:
            ValueError если проект не найден
        """
        return self._storage.get_project(project_id)
    
    def update_project_status(self, project_id: str, status: str) -> Project:
        """
        Обновляет статус проекта.
        
        Args:
            project_id: ID проекта
            status: Новый статус проекта
            
        Returns:
            Обновленный Project объект
            
        Raises:
            ValueError если статус невалидный или проект не найден
        """
        valid_statuses = {"created", "active", "paused", "completed", "failed"}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Must be one of {valid_statuses}")
        
        project = self._storage.get_project(project_id)
        project.status = status
        project.updated_at = datetime.now()
        self._storage.save_project(project)
        return project
    
    def set_active_job(self, project_id: str, job_id: str) -> Project:
        """
        Устанавливает активный job для проекта.
        
        Args:
            project_id: ID проекта
            job_id: ID активного job
            
        Returns:
            Обновленный Project объект
        """
        project = self._storage.get_project(project_id)
        project.active_job_id = job_id
        project.updated_at = datetime.now()
        self._storage.save_project(project)
        return project
    
    @staticmethod
    def _generate_project_id() -> str:
        """
        Генерирует уникальный ID для проекта.
        
        Returns:
            Уникальный строковый ID
        """
        import uuid
        return f"proj_{uuid.uuid4().hex}"
