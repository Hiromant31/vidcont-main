"""
Status manager for handling status transitions.
"""

from typing import Set


class StatusManager:
    """
    Менеджер для управления статусами сущностей.
    
    Предоставляет валидацию и допустимые переходы между статусами.
    """
    
    # Valid project statuses
    PROJECT_STATUSES: Set[str] = {"created", "active", "paused", "completed", "failed"}
    
    # Valid job statuses
    JOB_STATUSES: Set[str] = {"queued", "running", "paused", "completed", "failed"}
    
    # Valid stage run statuses
    STAGE_RUN_STATUSES: Set[str] = {"pending", "running", "completed", "failed", "retrying", "skipped"}
    
    # Allowed status transitions for projects
    PROJECT_TRANSITIONS = {
        "created": {"active", "failed"},
        "active": {"paused", "completed", "failed"},
        "paused": {"active", "completed", "failed"},
        "completed": set(),  # Terminal state
        "failed": set()  # Terminal state
    }
    
    # Allowed status transitions for jobs
    JOB_TRANSITIONS = {
        "queued": {"running", "failed"},
        "running": {"paused", "completed", "failed"},
        "paused": {"running", "completed", "failed"},
        "completed": set(),  # Terminal state
        "failed": set()  # Terminal state
    }
    
    # Allowed status transitions for stage runs
    STAGE_RUN_TRANSITIONS = {
        "pending": {"running", "skipped"},
        "running": {"completed", "failed", "retrying"},
        "completed": set(),  # Terminal state
        "failed": {"retrying"},
        "retrying": {"running", "failed"},
        "skipped": set()  # Terminal state
    }
    
    @classmethod
    def is_valid_project_status(cls, status: str) -> bool:
        """Проверяет валидность статуса проекта."""
        return status in cls.PROJECT_STATUSES
    
    @classmethod
    def is_valid_job_status(cls, status: str) -> bool:
        """Проверяет валидность статуса job."""
        return status in cls.JOB_STATUSES
    
    @classmethod
    def is_valid_stage_run_status(cls, status: str) -> bool:
        """Проверяет валидность статуса stage run."""
        return status in cls.STAGE_RUN_STATUSES
    
    @classmethod
    def can_transition_project(cls, from_status: str, to_status: str) -> bool:
        """
        Проверяет допустимость перехода между статусами проекта.
        
        Args:
            from_status: Текущий статус
            to_status: Целевой статус
            
        Returns:
            True если переход допустим
        """
        if from_status not in cls.PROJECT_TRANSITIONS:
            return False
        return to_status in cls.PROJECT_TRANSITIONS[from_status]
    
    @classmethod
    def can_transition_job(cls, from_status: str, to_status: str) -> bool:
        """
        Проверяет допустимость перехода между статусами job.
        
        Args:
            from_status: Текущий статус
            to_status: Целевой статус
            
        Returns:
            True если переход допустим
        """
        if from_status not in cls.JOB_TRANSITIONS:
            return False
        return to_status in cls.JOB_TRANSITIONS[from_status]
    
    @classmethod
    def can_transition_stage_run(cls, from_status: str, to_status: str) -> bool:
        """
        Проверяет допустимость перехода между статусами stage run.
        
        Args:
            from_status: Текущий статус
            to_status: Целевой статус
            
        Returns:
            True если переход допустим
        """
        if from_status not in cls.STAGE_RUN_TRANSITIONS:
            return False
        return to_status in cls.STAGE_RUN_TRANSITIONS[from_status]
