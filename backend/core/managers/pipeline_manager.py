"""
Pipeline manager for orchestrating video generation pipeline.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from ..models import Job, StageRun
from ..interfaces import StorageInterface
from ..executors import StageExecutor, STAGES


class PipelineManager:
    """
    Менеджер для управления выполнением pipeline.
    
    Orchestrates execution of all stages in the correct order.
    """
    
    def __init__(
        self,
        job_manager: "JobManager",
        stage_executor: StageExecutor,
        context_builder: "ContextBuilder",
        event_logger: "EventLogger"
    ):
        """
        Инициализирует PipelineManager.
        
        Args:
            job_manager: JobManager instance
            stage_executor: StageExecutor instance
            context_builder: ContextBuilder instance
            event_logger: EventLogger instance
        """
        self._job_manager = job_manager
        self._stage_executor = stage_executor
        self._context_builder = context_builder
        self._event_logger = event_logger
    
    def run_pipeline(
        self,
        job_id: str,
        start_stage: Optional[str] = None,
        auto_continue: bool = True
    ) -> Dict[str, Any]:
        """
        Запускает pipeline execution.
        
        Args:
            job_id: ID задачи
            start_stage: с какого этапа начать (None = с начала)
            auto_continue: автоматически идти дальше или остановиться после этапа
            
        Returns:
            {
                "status": "completed" | "failed" | "paused",
                "current_stage": str,
                "error": str | None
            }
            
        Logic:
            1. start_job
            2. for each stage in STAGES (начиная с start_stage):
                - run_stage
                - if failed and no retry: break
                - if not auto_continue: break after first stage
            3. complete_job или fail_job
        """
        # Start the job
        job = self._job_manager.start_job(job_id)
        self._event_logger.log_event("job_started", job_id)
        
        # Determine starting stage index
        start_index = 0
        if start_stage:
            if start_stage not in STAGES:
                raise ValueError(f"Invalid start_stage '{start_stage}'")
            start_index = STAGES.index(start_stage)
        
        current_stage = None
        error = None
        
        try:
            for i in range(start_index, len(STAGES)):
                stage_name = STAGES[i]
                current_stage = stage_name
                
                # Build context for this stage
                context = self._context_builder.build_context(job_id, stage_name)
                
                # Execute stage
                stage_run = self._stage_executor.execute_stage(job_id, stage_name, context)
                
                # Update job's current stage
                self._job_manager.update_job_stage(job_id, stage_name)
                
                # Check if stage failed
                if stage_run.status == "failed":
                    error = stage_run.error
                    self._job_manager.fail_job(job_id, error)
                    self._event_logger.log_event("job_failed", job_id, stage_name, error)
                    return {
                        "status": "failed",
                        "current_stage": stage_name,
                        "error": error
                    }
                
                # If not auto_continue, stop after first stage
                if not auto_continue:
                    return {
                        "status": "paused",
                        "current_stage": stage_name,
                        "error": None
                    }
            
            # All stages completed successfully
            self._job_manager.complete_job(job_id)
            self._event_logger.log_event("job_completed", job_id)
            
            return {
                "status": "completed",
                "current_stage": STAGES[-1] if STAGES else None,
                "error": None
            }
            
        except Exception as e:
            error = str(e)
            self._job_manager.fail_job(job_id, error)
            self._event_logger.log_event("job_failed", job_id, current_stage, error)
            
            return {
                "status": "failed",
                "current_stage": current_stage,
                "error": error
            }
    
    def run_next_stage(self, job_id: str) -> StageRun:
        """
        Запускает следующий этап для job.
        
        Args:
            job_id: ID задачи
            
        Returns:
            StageRun результат выполнения
            
        Logic:
            1. get current_stage from job
            2. find next stage in STAGES
            3. execute it
            4. update job.current_stage
        """
        job = self._job_manager.get_job(job_id)
        
        # Find next stage
        next_stage = None
        if job.current_stage is None:
            next_stage = STAGES[0]
        else:
            current_index = STAGES.index(job.current_stage)
            if current_index < len(STAGES) - 1:
                next_stage = STAGES[current_index + 1]
        
        if next_stage is None:
            raise ValueError("No more stages to run")
        
        # Build context and execute
        context = self._context_builder.build_context(job_id, next_stage)
        stage_run = self._stage_executor.execute_stage(job_id, next_stage, context)
        
        # Update job's current stage
        self._job_manager.update_job_stage(job_id, next_stage)
        
        return stage_run
