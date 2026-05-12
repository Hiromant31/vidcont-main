"""Analytics API Routes"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from api.schemas.analytics_schema import (
    AnalyticsOverview, PipelineMetrics, JobMetrics,
    RenderMetrics, SystemLoadMetrics
)
from analytics.analytics_manager import AnalyticsManager

router = APIRouter()
analytics_manager = AnalyticsManager()


@router.get("/overview", response_model=AnalyticsOverview, tags=["Analytics"])
async def get_overview(
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    project_id: Optional[str] = Query(None, description="Filter by project")
):
    """Get overall analytics statistics."""
    try:
        return analytics_manager.get_overview(
            date_from=date_from,
            date_to=date_to,
            project_id=project_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get overview: {str(e)}")


@router.get("/pipeline", response_model=PipelineMetrics, tags=["Analytics"])
async def get_pipeline_stats(
    date_from: Optional[str] = Query(None, description="Start date"),
    date_to: Optional[str] = Query(None, description="End date"),
    stage: Optional[str] = Query(None, description="Filter by pipeline stage")
):
    """Get pipeline statistics and stage breakdown."""
    try:
        return analytics_manager.get_pipeline_stats(
            date_from=date_from,
            date_to=date_to,
            stage=stage
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pipeline stats: {str(e)}")


@router.get("/jobs", response_model=JobMetrics, tags=["Analytics"])
async def get_jobs_stats(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Get jobs distribution statistics."""
    try:
        return analytics_manager.get_jobs_stats(
            date_from=date_from,
            date_to=date_to,
            status=status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get jobs stats: {str(e)}")


@router.get("/render", response_model=RenderMetrics, tags=["Analytics"])
async def get_render_stats(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None)
):
    """Get render statistics."""
    try:
        return analytics_manager.get_render_stats(
            date_from=date_from,
            date_to=date_to
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get render stats: {str(e)}")


@router.get("/system", response_model=SystemLoadMetrics, tags=["Analytics"])
async def get_system_load():
    """Get current system load metrics."""
    try:
        return analytics_manager.get_system_load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system load: {str(e)}")
