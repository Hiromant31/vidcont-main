"""
Render API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from datetime import datetime

from api.schemas.render_schema import (
    StartRenderRequest,
    RenderJobResponse,
    CheckStatusRequest,
    StopRenderRequest,
    ConnectServerRequest,
    ServerConnectionResponse,
    HealthCheckRequest,
    HealthCheckResponse,
    UploadAssetsRequest,
    UploadResultResponse,
    DownloadResultRequest,
)
from render.render_manager import RenderManager
from render.colab_client import ColabClient
from render.server_health import ServerHealth
from render.upload_manager import UploadManager
from render.result_downloader import ResultDownloader

router = APIRouter()

# Initialize modules
colab_client = ColabClient()
render_manager = RenderManager(colab_client)
server_health = ServerHealth(colab_client)
upload_manager = UploadManager(colab_client)
result_downloader = ResultDownloader(colab_client)


@router.post("/start", response_model=RenderJobResponse, tags=["Render"])
async def start_render(request: StartRenderRequest):
    """
    Start a render job on Colab server.
    
    Uploads assets and starts the video rendering process.
    """
    try:
        # Create render payload
        from render.render_schema import RenderPayload
        payload = RenderPayload(
            manifest=request.manifest,
            assets=request.assets,
            background_music=request.background_music
        )
        
        render_job = render_manager.start_render(
            job_id=request.job_id,
            colab_url=request.colab_url,
            render_payload=payload
        )
        
        return RenderJobResponse(
            render_job_id=render_job.render_job_id,
            job_id=render_job.job_id,
            colab_url=render_job.colab_url,
            status=render_job.status.value,
            progress=render_job.progress,
            result_video_url=render_job.result_video_url,
            logs=render_job.logs,
            created_at=render_job.created_at,
            updated_at=render_job.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Render start failed: {str(e)}")


@router.post("/status", tags=["Render"])
async def check_status(request: CheckStatusRequest):
    """
    Check status of a running render job.
    """
    try:
        render_job = render_manager.check_status(request.render_job_id)
        
        return {
            "render_job_id": render_job.render_job_id,
            "job_id": render_job.job_id,
            "status": render_job.status.value,
            "progress": render_job.progress,
            "result_video_url": render_job.result_video_url,
            "logs": render_job.logs,
            "updated_at": render_job.updated_at
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.post("/stop", tags=["Render"])
async def stop_render(request: StopRenderRequest):
    """
    Stop a running render job.
    """
    try:
        result = render_manager.stop_render(request.render_job_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stop failed: {str(e)}")


@router.get("/job/{render_job_id}", response_model=RenderJobResponse, tags=["Render"])
async def get_render_job(render_job_id: str):
    """
    Get render job details by ID.
    """
    try:
        render_job = render_manager.get_job(render_job_id)
        if not render_job:
            raise HTTPException(status_code=404, detail="Render job not found")
        
        return RenderJobResponse(
            render_job_id=render_job.render_job_id,
            job_id=render_job.job_id,
            colab_url=render_job.colab_url,
            status=render_job.status.value,
            progress=render_job.progress,
            result_video_url=render_job.result_video_url,
            logs=render_job.logs,
            created_at=render_job.created_at,
            updated_at=render_job.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job: {str(e)}")


@router.post("/connect-server", response_model=ServerConnectionResponse, tags=["Render"])
async def connect_server(request: ConnectServerRequest):
    """
    Connect to Colab server and verify connection.
    """
    try:
        result = colab_client.connect_server(request.colab_url, request.timeout)
        
        return ServerConnectionResponse(
            connected=result.get("connected", False),
            server_info=result.get("server_info", {}),
            latency_ms=result.get("latency_ms", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")


@router.post("/health-check", response_model=HealthCheckResponse, tags=["Render"])
async def health_check(request: HealthCheckRequest):
    """
    Perform health check on Colab server.
    """
    try:
        result = server_health.health_check(request.colab_url)
        
        return HealthCheckResponse(
            healthy=result.get("healthy", False),
            gpu_available=result.get("gpu_available", False),
            memory_available_gb=result.get("memory_available_gb", 0.0),
            disk_available_gb=result.get("disk_available_gb", 0.0),
            ffmpeg_version=result.get("ffmpeg_version", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.post("/upload-assets", response_model=UploadResultResponse, tags=["Render"])
async def upload_assets(request: UploadAssetsRequest):
    """
    Upload assets to Colab server.
    """
    try:
        result = upload_manager.upload_render_pack(
            request.colab_url,
            {"assets": request.assets, "asset_type": request.asset_type}
        )
        
        return UploadResultResponse(
            uploaded_count=len(result.get("uploaded_paths", [])),
            uploaded_paths=result.get("uploaded_paths", []),
            failed_uploads=result.get("failed_uploads", []),
            total_size_mb=result.get("total_size_mb", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/download-result", tags=["Render"])
async def download_result(request: DownloadResultRequest):
    """
    Download rendered video from Colab server.
    """
    try:
        result = result_downloader.download_result(
            request.render_job_id,
            request.colab_url,
            request.output_path
        )
        
        return {
            "download_path": result.get("download_path", ""),
            "file_size_mb": result.get("file_size_mb", 0.0),
            "download_time_sec": result.get("download_time_sec", 0.0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.delete("/job/{render_job_id}/cleanup", tags=["Render"])
async def cleanup_job(render_job_id: str):
    """
    Clean up completed render job from active jobs.
    """
    try:
        result = render_manager.cleanup_job(render_job_id)
        if result:
            return {"message": f"Job {render_job_id} cleaned up successfully"}
        else:
            raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")
