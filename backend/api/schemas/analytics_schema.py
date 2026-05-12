"""Analytics API Schemas"""
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime


class StageBreakdown(BaseModel):
    success: int = 0
    failed: int = 0
    avg_time: float = 0.0


class PipelineMetrics(BaseModel):
    total_runs: int = 0
    success_rate: float = 0.0
    failure_rate: float = 0.0
    avg_duration_sec: float = 0.0
    stage_breakdown: Dict[str, StageBreakdown] = {}


class JobMetrics(BaseModel):
    total_jobs: int = 0
    queued: int = 0
    running: int = 0
    completed: int = 0
    failed: int = 0
    avg_processing_time: float = 0.0


class RenderMetrics(BaseModel):
    total_renders: int = 0
    success_rate: float = 0.0
    avg_render_time_sec: float = 0.0
    avg_video_length_sec: float = 0.0
    resolution_distribution: Dict[str, int] = {}


class SystemLoadMetrics(BaseModel):
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    active_connections: int = 0
    queue_size: int = 0
    throughput_per_min: float = 0.0


class AnalyticsOverview(BaseModel):
    total_projects: int = 0
    total_jobs: int = 0
    total_renders: int = 0
    global_success_rate: float = 0.0
    total_errors: int = 0
    estimated_cost_usd: float = 0.0
