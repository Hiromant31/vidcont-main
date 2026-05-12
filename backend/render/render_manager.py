"""
Render Manager - Orchestrates the render process on Colab server
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from .render_schema import RenderJob, JobStatus, RenderPayload, ColabServer
from .colab_client import ColabClient
from .upload_manager import UploadManager


class RenderManager:
    """Manages render job lifecycle on Colab server"""

    def __init__(self, colab_client: ColabClient):
        self.colab_client = colab_client
        self.upload_manager = UploadManager(colab_client)
        self.active_jobs: Dict[str, RenderJob] = {}

    def start_render(
        self,
        job_id: str,
        colab_url: str,
        render_payload: RenderPayload
    ) -> RenderJob:
        """
        Start render job on Colab server.

        INPUT:
        {
            "job_id": string,
            "colab_url": string,
            "render_payload": RenderPayload
        }

        OUTPUT:
        RenderJob

        RULE:
        👉 этот вызов запускает pipeline на Colab сервере
        """
        render_job_id = str(uuid.uuid4())

        # Create render job record
        render_job = RenderJob(
            render_job_id=render_job_id,
            job_id=job_id,
            colab_url=colab_url,
            status=JobStatus.UPLOADING,
            progress=0.0
        )

        try:
            # Step 1: Upload assets
            payload_dict = render_payload.to_dict()
            upload_result = self.upload_manager.upload_render_pack(
                colab_url,
                payload_dict
            )

            # Update paths in payload with uploaded paths
            if "uploaded_paths" in upload_result:
                render_payload.assets = upload_result["uploaded_paths"]

            # Step 2: Start render on Colab
            render_job.status = JobStatus.RUNNING
            render_job.updated_at = datetime.now()

            response = self.colab_client.start_render(colab_url, payload_dict)

            # Store job
            self.active_jobs[render_job_id] = render_job

            return render_job

        except Exception as e:
            render_job.status = JobStatus.FAILED
            render_job.logs.append(f"Start failed: {str(e)}")
            render_job.updated_at = datetime.now()
            self.active_jobs[render_job_id] = render_job
            raise

    def check_status(self, render_job_id: str) -> RenderJob:
        """
        Check status of running render job.

        INPUT:
        {
            "render_job_id": string
        }

        OUTPUT:
        RenderJob
        """
        if render_job_id not in self.active_jobs:
            raise ValueError(f"Render job not found: {render_job_id}")

        render_job = self.active_jobs[render_job_id]

        try:
            status_data = self.colab_client.get_status(
                render_job.colab_url,
                render_job_id
            )

            # Update job status
            status_str = status_data.get("status", "unknown")
            render_job.status = JobStatus(status_str) if status_str in [s.value for s in JobStatus] else JobStatus.UNKNOWN
            render_job.progress = status_data.get("progress", 0.0)
            render_job.updated_at = datetime.now()

            # Handle completion
            if render_job.status == JobStatus.COMPLETED:
                render_job.result_video_url = status_data.get("video_url")

            # Handle failure
            if render_job.status == JobStatus.FAILED:
                render_job.logs.extend(status_data.get("errors", []))

            self.active_jobs[render_job_id] = render_job
            return render_job

        except Exception as e:
            render_job.logs.append(f"Status check failed: {str(e)}")
            render_job.updated_at = datetime.now()
            return render_job

    def stop_render(self, render_job_id: str) -> Dict[str, str]:
        """
        Stop running render job.

        INPUT:
        {
            "render_job_id": string
        }

        OUTPUT:
        {
            "status": "stopped"
        }
        """
        if render_job_id not in self.active_jobs:
            raise ValueError(f"Render job not found: {render_job_id}")

        render_job = self.active_jobs[render_job_id]

        result = self.colab_client.stop_render(render_job.colab_url, render_job_id)

        if result.get("status") == "stopped":
            render_job.status = JobStatus.FAILED
            render_job.logs.append("Render stopped by user")
            render_job.updated_at = datetime.now()
            self.active_jobs[render_job_id] = render_job

        return result

    def get_job(self, render_job_id: str) -> Optional[RenderJob]:
        """Get render job by ID"""
        return self.active_jobs.get(render_job_id)

    def cleanup_job(self, render_job_id: str) -> bool:
        """Remove job from active jobs (after download)"""
        if render_job_id in self.active_jobs:
            del self.active_jobs[render_job_id]
            return True
        return False
