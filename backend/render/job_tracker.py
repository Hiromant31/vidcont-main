"""
Job Tracker - Tracks and manages render job history
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .render_schema import RenderJob, JobStatus


class JobTracker:
    """Tracks render job history and provides monitoring"""

    def __init__(self, max_history_hours: int = 24):
        self.job_history: Dict[str, RenderJob] = {}
        self.max_history_hours = max_history_hours

    def track_job(self, render_job: RenderJob) -> None:
        """Add or update job in tracker"""
        self.job_history[render_job.render_job_id] = render_job

    def get_job(self, render_job_id: str) -> Optional[RenderJob]:
        """Get job by ID from history"""
        return self.job_history.get(render_job_id)

    def get_jobs_by_status(self, status: JobStatus) -> List[RenderJob]:
        """Get all jobs with specific status"""
        return [
            job for job in self.job_history.values()
            if job.status == status
        ]

    def get_active_jobs(self) -> List[RenderJob]:
        """Get all currently active jobs"""
        active_statuses = [
            JobStatus.QUEUED,
            JobStatus.UPLOADING,
            JobStatus.RUNNING,
            JobStatus.PROCESSING
        ]
        return [
            job for job in self.job_history.values()
            if job.status in active_statuses
        ]

    def get_completed_jobs(self, hours: int = 24) -> List[RenderJob]:
        """Get completed jobs from last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            job for job in self.job_history.values()
            if job.status == JobStatus.COMPLETED
            and job.updated_at > cutoff
        ]

    def get_failed_jobs(self, hours: int = 24) -> List[RenderJob]:
        """Get failed jobs from last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            job for job in self.job_history.values()
            if job.status == JobStatus.FAILED
            and job.updated_at > cutoff
        ]

    def cleanup_old_jobs(self) -> int:
        """Remove jobs older than max_history_hours"""
        cutoff = datetime.now() - timedelta(hours=self.max_history_hours)
        old_jobs = [
            job_id for job_id, job in self.job_history.items()
            if job.updated_at < cutoff
            and job.status in [JobStatus.COMPLETED, JobStatus.FAILED]
        ]

        for job_id in old_jobs:
            del self.job_history[job_id]

        return len(old_jobs)

    def get_statistics(self) -> Dict[str, any]:
        """Get render statistics"""
        total = len(self.job_history)
        completed = len(self.get_jobs_by_status(JobStatus.COMPLETED))
        failed = len(self.get_jobs_by_status(JobStatus.FAILED))
        active = len(self.get_active_jobs())

        return {
            "total_jobs": total,
            "completed": completed,
            "failed": failed,
            "active": active,
            "success_rate": (completed / total * 100) if total > 0 else 0
        }
