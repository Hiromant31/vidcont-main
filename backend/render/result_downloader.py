"""
Result Downloader - Downloads completed render results from Colab server
"""

import os
from typing import Dict, Any
from .render_schema import RenderResult, RenderJob, JobStatus
from .colab_client import ColabClient


class ResultDownloader:
    """Handles downloading of completed render results"""

    def __init__(self, colab_client: ColabClient):
        self.colab_client = colab_client

    def download_result(self, render_job: RenderJob, save_path: str) -> RenderResult:
        """
        Download rendered video file.

        INPUT:
        {
            "render_job_id": string
        }

        OUTPUT:
        RenderResult
        """
        if render_job.status != JobStatus.COMPLETED:
            raise ValueError(
                f"Cannot download incomplete job. Status: {render_job.status.value}"
            )

        try:
            # Download the video file
            downloaded_path = self.colab_client.download_result(
                render_job.colab_url,
                render_job.render_job_id,
                save_path
            )

            # Get file size for duration estimation (if not available)
            file_size = os.path.getsize(downloaded_path)

            return RenderResult(
                render_job_id=render_job.render_job_id,
                video_path=downloaded_path,
                duration_sec=0.0,  # Will be calculated from actual video
                resolution="unknown",  # Will be extracted from video metadata
                status="success"
            )

        except Exception as e:
            return RenderResult(
                render_job_id=render_job.render_job_id,
                video_path="",
                duration_sec=0.0,
                resolution="unknown",
                status="failed"
            )

    def download_with_retry(
        self,
        render_job: RenderJob,
        save_path: str,
        max_retries: int = 3
    ) -> RenderResult:
        """Download with retry logic for transient failures"""
        last_error = None

        for attempt in range(max_retries):
            try:
                result = self.download_result(render_job, save_path)
                if result.status == "success":
                    return result
                last_error = Exception("Download returned failed status")
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    continue  # Retry

        # All retries failed
        return RenderResult(
            render_job_id=render_job.render_job_id,
            video_path="",
            duration_sec=0.0,
            resolution="unknown",
            status="failed"
        )

    def verify_download(self, result: RenderResult) -> bool:
        """Verify that downloaded file exists and has content"""
        if not result.video_path:
            return False

        if not os.path.exists(result.video_path):
            return False

        file_size = os.path.getsize(result.video_path)
        return file_size > 0
