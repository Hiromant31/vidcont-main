"""
Queue Manager - Управление очередью задач
"""
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from core.logger import setup_logger

logger = setup_logger(__name__)

class QueueManager:
    """Менеджер очереди задач"""
    
    def __init__(self, max_concurrent_jobs: int = 3):
        self.max_concurrent = max_concurrent_jobs
        self.queue: asyncio.Queue = asyncio.Queue()
        self.running_jobs: Dict[str, Dict] = {}
        self.job_status: Dict[str, str] = {}
    
    async def add_job(self, job_id: str, priority: int = 0) -> bool:
        """Добавить задачу в очередь"""
        await self.queue.put({
            "job_id": job_id,
            "priority": priority,
            "added_at": datetime.now()
        })
        self.job_status[job_id] = "queued"
        logger.info(f"Job {job_id} added to queue with priority {priority}")
        return True
    
    async def get_next_job(self) -> Optional[Dict]:
        """Получить следующую задачу из очереди"""
        if len(self.running_jobs) >= self.max_concurrent:
            return None
        
        try:
            job_info = self.queue.get_nowait()
            return job_info
        except asyncio.QueueEmpty:
            return None
    
    def start_job(self, job_id: str):
        """Отметить задачу как запущенную"""
        self.running_jobs[job_id] = {
            "started_at": datetime.now(),
            "status": "running"
        }
        self.job_status[job_id] = "running"
        logger.debug(f"Job {job_id} started")
    
    def complete_job(self, job_id: str):
        """Отметить задачу как завершенную"""
        if job_id in self.running_jobs:
            del self.running_jobs[job_id]
        self.job_status[job_id] = "completed"
        logger.debug(f"Job {job_id} completed")
    
    def fail_job(self, job_id: str, error: str):
        """Отметить задачу как failed"""
        if job_id in self.running_jobs:
            self.running_jobs[job_id]["error"] = error
            del self.running_jobs[job_id]
        self.job_status[job_id] = "failed"
        logger.error(f"Job {job_id} failed: {error}")
    
    def get_queue_status(self) -> Dict:
        """Получить статус очереди"""
        return {
            "queued": self.queue.qsize(),
            "running": len(self.running_jobs),
            "max_concurrent": self.max_concurrent,
            "jobs": list(self.job_status.values())
        }
    
    async def process_queue(self):
        """Обработка очереди (фоновый процесс)"""
        while True:
            job_info = await self.get_next_job()
            
            if job_info:
                job_id = job_info["job_id"]
                self.start_job(job_id)
                # Здесь будет логика запуска пайплайна
                logger.info(f"Processing job {job_id} from queue")
            else:
                await asyncio.sleep(1)
