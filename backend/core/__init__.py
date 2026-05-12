"""
Core system for AI video generation platform.

This module provides the orchestration layer for video generation pipelines.
It manages projects, jobs, and stage execution WITHOUT implementing actual
content generation (LLM, TTS, image generation, rendering, etc.).

Architecture:
    - models: Data classes for Project, Job, StageRun
    - interfaces: Abstract base classes (StageInterface, StorageInterface)
    - managers: Business logic (ProjectManager, JobManager, PipelineManager)
    - executors: Stage execution (StageExecutor, StageRegistry)
    - utils: Utilities (RetryManager, ContextBuilder, EventLogger, StatusManager)

Key Principles:
    - NO content generation logic
    - ONLY orchestration and state management
    - Dependency injection for all external dependencies
    - Strict API contracts as defined in blueprint
"""

from .models import Project, Job, StageRun
from .interfaces import StageInterface, StorageInterface
from .managers import ProjectManager, JobManager, PipelineManager
from .executors import StageExecutor, StageRegistry, STAGES, validate_stage_name
from .utils import (
    StatusManager,
    RetryManager,
    ContextBuilder,
    EventLogger
)


def init_core_system(storage: StorageInterface) -> dict:
    """
    Инициализация всех компонентов core system.
    
    Args:
        storage: StorageInterface implementation
        
    Returns:
        Dict с инициализированными компонентами:
        {
            "project_manager": ProjectManager,
            "job_manager": JobManager,
            "pipeline_manager": PipelineManager,
            "stage_registry": StageRegistry
        }
    """
    # Utilities
    event_logger = EventLogger()
    retry_manager = RetryManager(max_retries=3)
    context_builder = ContextBuilder(storage, event_logger)
    
    # Registry
    stage_registry = StageRegistry()
    
    # Managers
    project_manager = ProjectManager(storage)
    job_manager = JobManager(storage)
    stage_executor = StageExecutor(
        stage_registry,
        retry_manager,
        event_logger,
        storage
    )
    pipeline_manager = PipelineManager(
        job_manager,
        stage_executor,
        context_builder,
        event_logger
    )
    
    return {
        "project_manager": project_manager,
        "job_manager": job_manager,
        "pipeline_manager": pipeline_manager,
        "stage_registry": stage_registry
    }


__all__ = [
    # Models
    "Project",
    "Job",
    "StageRun",
    
    # Interfaces
    "StageInterface",
    "StorageInterface",
    
    # Managers
    "ProjectManager",
    "JobManager",
    "PipelineManager",
    
    # Executors
    "StageExecutor",
    "StageRegistry",
    "STAGES",
    "validate_stage_name",
    
    # Utils
    "StatusManager",
    "RetryManager",
    "ContextBuilder",
    "EventLogger",
    
    # Initialization
    "init_core_system"
]
