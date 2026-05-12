"""
Job data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Job:
    """
    Job entity representing a video generation job within a project.
    
    Attributes:
        job_id: Unique identifier for the job
        project_id: Reference to the parent project
        status: Current status of the job
        current_stage: Name of the currently executing stage (if any)
        created_at: Timestamp when job was created
        started_at: Timestamp when job execution started
        finished_at: Timestamp when job execution completed
        error: Error message if job failed
    """
    job_id: str
    project_id: str
    status: str  # "queued" | "running" | "paused" | "completed" | "failed"
    current_stage: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    error: Optional[str]
    
    def __post_init__(self):
        """Validate status values."""
        valid_statuses = {"queued", "running", "paused", "completed", "failed"}
        if self.status not in valid_statuses:
            raise ValueError(f"Invalid status '{self.status}'. Must be one of {valid_statuses}")
