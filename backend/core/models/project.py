"""
Project data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """
    Project entity representing a video generation project.
    
    Attributes:
        project_id: Unique identifier for the project
        name: Human-readable project name
        status: Current status of the project
        settings_id: Reference to settings configuration
        active_job_id: ID of the currently active job (if any)
        created_at: Timestamp when project was created
        updated_at: Timestamp when project was last updated
    """
    project_id: str
    name: str
    status: str  # "created" | "active" | "paused" | "completed" | "failed"
    settings_id: str
    active_job_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validate status values."""
        valid_statuses = {"created", "active", "paused", "completed", "failed"}
        if self.status not in valid_statuses:
            raise ValueError(f"Invalid status '{self.status}'. Must be one of {valid_statuses}")
