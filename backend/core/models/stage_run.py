"""
StageRun data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class StageRun:
    """
    StageRun entity representing a single stage execution within a job.
    
    Attributes:
        stage_run_id: Unique identifier for this stage run
        job_id: Reference to the parent job
        stage_name: Name of the stage being executed
        status: Current status of the stage execution
        retry_count: Number of retry attempts made
        input_context: Input data passed to the stage
        output_data: Output data produced by the stage
        error: Error message if stage failed
        started_at: Timestamp when stage execution started
        finished_at: Timestamp when stage execution completed
    """
    stage_run_id: str
    job_id: str
    stage_name: str
    status: str  # "pending" | "running" | "completed" | "failed" | "retrying" | "skipped"
    retry_count: int
    input_context: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    error: Optional[str]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    
    def __post_init__(self):
        """Validate status values."""
        valid_statuses = {"pending", "running", "completed", "failed", "retrying", "skipped"}
        if self.status not in valid_statuses:
            raise ValueError(f"Invalid status '{self.status}'. Must be one of {valid_statuses}")
