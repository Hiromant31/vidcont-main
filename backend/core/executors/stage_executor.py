"""
Stage executor for executing individual pipeline stages.
"""

from datetime import datetime
from typing import Dict, Any

from ..models import StageRun
from ..interfaces import StorageInterface
from .stage_registry import StageRegistry, validate_stage_name
from ..utils import RetryManager, EventLogger


class StageExecutor:
    """
    Исполнитель для отдельных этапов pipeline.
    
    Отвечает за выполнение stage с обработкой ошибок и retry logic.
    """
    
    def __init__(
        self,
        stage_registry: StageRegistry,
        retry_manager: RetryManager,
        event_logger: EventLogger,
        storage: StorageInterface
    ):
        """
        Инициализирует StageExecutor.
        
        Args:
            stage_registry: StageRegistry instance
            retry_manager: RetryManager instance
            event_logger: EventLogger instance
            storage: StorageInterface instance
        """
        self._stage_registry = stage_registry
        self._retry_manager = retry_manager
        self._event_logger = event_logger
        self._storage = storage
    
    def execute_stage(
        self,
        job_id: str,
        stage_name: str,
        context: Dict[str, Any]
    ) -> StageRun:
        """
        Выполняет один этап pipeline.
        
        Args:
            job_id: ID задачи
            stage_name: имя этапа из STAGES
            context: входные данные для этапа
            
        Returns:
            StageRun с результатом выполнения
            
        Logic:
            1. create StageRun (status="pending")
            2. validate stage_name
            3. get stage implementation from registry
            4. try:
                - status = "running"
                - output = stage.execute(context)
                - status = "completed"
            5. except Exception:
                - status = "failed"
                - check retry_manager
                - if should_retry: status = "retrying", retry
            6. save and return StageRun
        """
        # Validate stage name
        if not validate_stage_name(stage_name):
            raise ValueError(f"Invalid stage name '{stage_name}'")
        
        # Create StageRun record
        stage_run = StageRun(
            stage_run_id=self._generate_stage_run_id(),
            job_id=job_id,
            stage_name=stage_name,
            status="pending",
            retry_count=0,
            input_context=context,
            output_data=None,
            error=None,
            started_at=None,
            finished_at=None
        )
        
        # Get stage implementation
        try:
            stage_impl = self._stage_registry.get_stage(stage_name)
        except KeyError as e:
            stage_run.status = "failed"
            stage_run.error = str(e)
            stage_run.finished_at = datetime.now()
            self._storage.save_stage_run(stage_run)
            self._event_logger.log_event("stage_failed", job_id, stage_name, str(e))
            return stage_run
        
        # Execute with retry support
        max_retries = self._retry_manager.max_retries
        
        while True:
            try:
                # Mark as running
                stage_run.status = "running"
                stage_run.started_at = datetime.now()
                self._storage.save_stage_run(stage_run)
                self._event_logger.log_event("stage_started", job_id, stage_name)
                
                # Execute the stage
                output = stage_impl.execute(context)
                
                # Mark as completed
                stage_run.status = "completed"
                stage_run.output_data = output
                stage_run.finished_at = datetime.now()
                self._storage.save_stage_run(stage_run)
                self._event_logger.log_event("stage_completed", job_id, stage_name)
                
                return stage_run
                
            except Exception as e:
                error_msg = str(e)
                stage_run.error = error_msg
                
                # Check if we should retry
                retry_info = self._retry_manager.should_retry(stage_run)
                
                if retry_info["retry"]:
                    # Retry logic
                    stage_run.retry_count += 1
                    stage_run.status = "retrying"
                    self._storage.save_stage_run(stage_run)
                    self._event_logger.log_event(
                        "stage_retrying",
                        job_id,
                        stage_name,
                        f"Retry {stage_run.retry_count}/{max_retries}: {error_msg}"
                    )
                    
                    # Wait before retry (exponential backoff)
                    import time
                    time.sleep(retry_info["delay_seconds"])
                    
                    # Continue to next iteration
                    continue
                else:
                    # No more retries, mark as failed
                    stage_run.status = "failed"
                    stage_run.finished_at = datetime.now()
                    self._storage.save_stage_run(stage_run)
                    self._event_logger.log_event(
                        "stage_failed",
                        job_id,
                        stage_name,
                        error_msg
                    )
                    
                    return stage_run
    
    @staticmethod
    def _generate_stage_run_id() -> str:
        """
        Генерирует уникальный ID для stage run.
        
        Returns:
            Уникальный строковый ID
        """
        import uuid
        return f"stage_{uuid.uuid4().hex}"
