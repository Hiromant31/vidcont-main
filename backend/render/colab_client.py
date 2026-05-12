"""
Colab Client - Handles HTTP communication with Colab render server
"""

import requests
from typing import Dict, Any, Optional
from .render_schema import ColabServer, ServerStatus


class ColabClient:
    """Client for communicating with Colab render server"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()

    def connect_server(self, colab_url: str) -> ColabServer:
        """
        Connect to Colab server and verify availability.

        INPUT:
        {
            "colab_url": string
        }

        OUTPUT:
        ColabServer
        """
        try:
            response = self.session.get(
                f"{colab_url}/health",
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return ColabServer(
                    server_id=data.get("server_id", "unknown"),
                    url=colab_url,
                    status=ServerStatus.ONLINE,
                    last_ping=None
                )
            else:
                return ColabServer(
                    server_id="unknown",
                    url=colab_url,
                    status=ServerStatus.OFFLINE,
                    last_ping=None
                )
        except requests.exceptions.RequestException:
            return ColabServer(
                server_id="unknown",
                url=colab_url,
                status=ServerStatus.OFFLINE,
                last_ping=None
            )

    def ping_server(self, colab_url: str) -> Dict[str, str]:
        """
        Ping server to check if it's online.

        INPUT:
        {
            "colab_url": string
        }

        OUTPUT:
        {
            "status": "online | offline"
        }
        """
        try:
            response = self.session.get(
                f"{colab_url}/ping",
                timeout=5
            )
            if response.status_code == 200:
                return {"status": "online"}
            else:
                return {"status": "offline"}
        except requests.exceptions.RequestException:
            return {"status": "offline"}

    def start_render(self, colab_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start render job on Colab server.

        POST /render
        """
        try:
            response = self.session.post(
                f"{colab_url}/render",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to start render: {str(e)}")

    def get_status(self, colab_url: str, render_job_id: str) -> Dict[str, Any]:
        """
        Get render job status.

        GET /status/{render_job_id}
        """
        try:
            response = self.session.get(
                f"{colab_url}/status/{render_job_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get status: {str(e)}")

    def stop_render(self, colab_url: str, render_job_id: str) -> Dict[str, str]:
        """
        Stop running render job.

        POST /stop/{render_job_id}
        """
        try:
            response = self.session.post(
                f"{colab_url}/stop/{render_job_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return {"status": "stopped"}
        except requests.exceptions.RequestException:
            return {"status": "stop_failed"}

    def download_result(self, colab_url: str, render_job_id: str, save_path: str) -> str:
        """
        Download rendered video file.

        GET /result/{render_job_id}
        """
        try:
            response = self.session.get(
                f"{colab_url}/result/{render_job_id}",
                timeout=self.timeout,
                stream=True
            )
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return save_path
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download result: {str(e)}")
