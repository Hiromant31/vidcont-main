"""
Pipeline Manager - Оркестрация этапов генерации видео
"""
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from api.schemas.pipeline_schema import PipelineResponse, PipelineStage, StageStatus
from orchestration.stage_runner import StageRunner
from core.logger import setup_logger

logger = setup_logger(__name__)

# Порядок этапов пайплайна
PIPELINE_STAGES = [
    "story_generation",
    "character_extraction",
    "scene_generation",
    "tts_generation",
    "manifest_build",
    "render"
]

class PipelineManager:
    """Менеджер оркестрации пайплайна"""
    
    def __init__(self):
        self.stage_runner = StageRunner()
        self.job_states: Dict[str, Dict[str, Any]] = {}
    
    async def execute_full_pipeline(self, job_id: str) -> bool:
        """Выполнить полный пайплайн для задачи"""
        logger.info(f"Starting full pipeline for job {job_id}")
        
        try:
            # Инициализация состояния задачи
            self._init_job_state(job_id)
            
            for stage_name in PIPELINE_STAGES:
                success = await self._execute_stage(job_id, stage_name)
                
                if not success:
                    logger.error(f"Pipeline failed at stage {stage_name}")
                    return False
            
            logger.info(f"Pipeline completed successfully for job {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Pipeline execution error: {e}")
            return False
    
    async def _execute_stage(self, job_id: str, stage_name: str) -> bool:
        """Выполнить один этап пайплайна"""
        logger.info(f"Executing stage {stage_name} for job {job_id}")
        
        # Обновление статуса этапа
        self._update_stage_status(job_id, stage_name, StageStatus.RUNNING)
        
        try:
            # Выполнение этапа через StageRunner
            result = await self.stage_runner.run_stage(stage_name, job_id, self.job_states[job_id])
            
            if result["success"]:
                self._update_stage_status(
                    job_id,
                    stage_name,
                    StageStatus.COMPLETED,
                    output=result.get("output")
                )
                # Сохранение выхода этапа в контекст
                self.job_states[job_id]["stage_outputs"][stage_name] = result.get("output")
                logger.info(f"Stage {stage_name} completed")
                return True
            else:
                self._update_stage_status(
                    job_id,
                    stage_name,
                    StageStatus.FAILED,
                    error=result.get("error", "Unknown error")
                )
                logger.error(f"Stage {stage_name} failed: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"Stage {stage_name} exception: {e}")
            self._update_stage_status(job_id, stage_name, StageStatus.FAILED, error=str(e))
            return False
    
    def run_pipeline(self, job_id: str, stages: Optional[List[str]] = None) -> Optional[PipelineResponse]:
        """Запустить пайплайн (синхронная версия для API)"""
        # Запуск асинхронно в фоне
        asyncio.create_task(self.execute_full_pipeline(job_id))
        return self._build_pipeline_response(job_id)
    
    def run_stage(self, job_id: str, stage_name: str) -> Optional[PipelineResponse]:
        """Запустить конкретный этап"""
        if stage_name not in PIPELINE_STAGES:
            raise ValueError(f"Invalid stage: {stage_name}")
        
        asyncio.create_task(self._execute_stage(job_id, stage_name))
        return self._build_pipeline_response(job_id)
    
    def pause_pipeline(self, job_id: str) -> bool:
        """Поставить пайплайн на паузу"""
        if job_id not in self.job_states:
            return False
        
        self.job_states[job_id]["status"] = "paused"
        logger.info(f"Pipeline paused for job {job_id}")
        return True
    
    def resume_pipeline(self, job_id: str) -> bool:
        """Возобновить пайплайн"""
        if job_id not in self.job_states:
            return False
        
        self.job_states[job_id]["status"] = "running"
        logger.info(f"Pipeline resumed for job {job_id}")
        return True
    
    def _init_job_state(self, job_id: str):
        """Инициализировать состояние задачи"""
        self.job_states[job_id] = {
            "job_id": job_id,
            "status": "running",
            "current_stage": None,
            "stages": {},
            "stage_outputs": {},
            "context": {},
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    
    def _update_stage_status(
        self,
        job_id: str,
        stage_name: str,
        status: str,
        output: Optional[Dict] = None,
        error: Optional[str] = None
    ):
        """Обновить статус этапа"""
        if job_id not in self.job_states:
            self._init_job_state(job_id)
        
        now = datetime.now()
        stage_data = self.job_states[job_id]["stages"].get(stage_name, {})
        
        stage_data["status"] = status
        if status == StageStatus.RUNNING:
            stage_data["started_at"] = now
        elif status in [StageStatus.COMPLETED, StageStatus.FAILED]:
            stage_data["completed_at"] = now
        
        if output:
            stage_data["output"] = output
        if error:
            stage_data["error"] = error
        
        self.job_states[job_id]["stages"][stage_name] = stage_data
        self.job_states[job_id]["current_stage"] = stage_name
        self.job_states[job_id]["updated_at"] = now
    
    def _build_pipeline_response(self, job_id: str) -> Optional[PipelineResponse]:
        """Построить ответ для API"""
        if job_id not in self.job_states:
            return None
        
        state = self.job_states[job_id]
        stages_list = []
        
        for stage_name in PIPELINE_STAGES:
            stage_data = state["stages"].get(stage_name, {})
            stages_list.append(PipelineStage(
                name=stage_name,
                status=stage_data.get("status", StageStatus.PENDING),
                started_at=stage_data.get("started_at"),
                completed_at=stage_data.get("completed_at"),
                output=stage_data.get("output"),
                error=stage_data.get("error")
            ))
        
        # Расчет прогресса
        completed = sum(1 for s in stages_list if s.status == StageStatus.COMPLETED)
        progress = (completed / len(PIPELINE_STAGES)) * 100
        
        return PipelineResponse(
            job_id=job_id,
            status=state["status"],
            current_stage=state["current_stage"],
            stages=stages_list,
            progress=progress,
            created_at=state["created_at"],
            updated_at=state["updated_at"]
        )
