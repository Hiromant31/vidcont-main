"""
Job Manager - Управление задачами генерации
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from api.schemas.job_schema import JobResponse, JobStatus
from orchestration.pipeline_manager import PipelineManager
from core.logger import setup_logger

logger = setup_logger(__name__)

class JobManager:
    """Менеджер задач генерации видео"""
    
    def __init__(self):
        self.jobs: Dict[str, JobResponse] = {}
        self.pipeline_manager = PipelineManager()
        self._running_tasks: Dict[str, asyncio.Task] = {}
    
    def create_job(
        self,
        project_id: str,
        idea: str,
        genre: str = "general",
        style: str = "cinematic",
        duration_target: int = 60,
        orientation: str = "vertical",
        resolution: str = "720p"
    ) -> JobResponse:
        """Создать новую задачу"""
        job_id = str(uuid.uuid4())
        now = datetime.now()
        
        job = JobResponse(
            job_id=job_id,
            project_id=project_id,
            status=JobStatus.QUEUED,
            current_stage=None,
            progress=0.0,
            created_at=now,
            updated_at=now,
            logs=[f"Job created with idea: {idea[:50]}..."],
            errors=[]
        )
        
        self.jobs[job_id] = job
        logger.info(f"Created job {job_id} for project {project_id}")
        return job
    
    def get_job(self, job_id: str) -> Optional[JobResponse]:
        """Получить задачу по ID"""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[JobResponse]:
        """Получить все задачи"""
        return list(self.jobs.values())
    
    def update_job_status(
        self,
        job_id: str,
        status: Optional[str] = None,
        current_stage: Optional[str] = None,
        progress: Optional[float] = None,
        log_entry: Optional[str] = None,
        error: Optional[str] = None
    ):
        """Обновить статус задачи"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        job.updated_at = datetime.now()
        
        if status:
            job.status = status
        if current_stage:
            job.current_stage = current_stage
        if progress is not None:
            job.progress = progress
        if log_entry:
            job.logs.append(log_entry)
        if error:
            job.errors.append(error)
        
        logger.debug(f"Updated job {job_id}: status={status}, stage={current_stage}, progress={progress}")
    
    async def run_pipeline_async(self, job_id: str):
        """Запустить пайплайн асинхронно"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        task = asyncio.create_task(self._run_pipeline_background(job_id))
        self._running_tasks[job_id] = task
        
        # Обновление статуса при ошибке
        try:
            await task
        except Exception as e:
            logger.error(f"Pipeline failed for job {job_id}: {e}")
            self.update_job_status(job_id, status=JobStatus.FAILED, error=str(e))
    
    async def _run_pipeline_background(self, job_id: str):
        """Фоновое выполнение пайплайна"""
        try:
            self.update_job_status(job_id, status=JobStatus.RUNNING)
            
            # Запуск пайплайна через PipelineManager
            result = await self.pipeline_manager.execute_full_pipeline(job_id)
            
            if result:
                self.update_job_status(
                    job_id,
                    status=JobStatus.COMPLETED,
                    progress=100.0,
                    log_entry="Pipeline completed successfully"
                )
            else:
                self.update_job_status(
                    job_id,
                    status=JobStatus.FAILED,
                    error="Pipeline execution failed"
                )
        except Exception as e:
            logger.error(f"Pipeline error for job {job_id}: {e}")
            self.update_job_status(
                job_id,
                status=JobStatus.FAILED,
                error=str(e)
            )
    
    def stop_job(self, job_id: str):
        """Остановить задачу"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        if job_id in self._running_tasks:
            self._running_tasks[job_id].cancel()
            del self._running_tasks[job_id]
        
        self.update_job_status(job_id, status=JobStatus.PAUSED)
        logger.info(f"Stopped job {job_id}")
    
    def retry_job(self, job_id: str):
        """Перезапустить задачу"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        job.status = JobStatus.QUEUED
        job.current_stage = None
        job.progress = 0.0
        job.errors = []
        job.updated_at = datetime.now()
        
        asyncio.create_task(self.run_pipeline_async(job_id))
        logger.info(f"Retried job {job_id}")
