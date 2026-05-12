"""
Server Health - Monitors Colab server health and availability
"""

import time
from datetime import datetime
from typing import Dict, Any
from .render_schema import ColabServer, ServerStatus
from .colab_client import ColabClient


class ServerHealth:
    """Monitors health of Colab render servers"""

    def __init__(self, colab_client: ColabClient):
        self.colab_client = colab_client
        self.server_cache: Dict[str, ColabServer] = {}

    def health_check(self, colab_url: str) -> Dict[str, Any]:
        """
        Check health of Colab server.

        INPUT:
        {
            "colab_url": string
        }

        OUTPUT:
        {
            "status": "online | offline | degraded",
            "latency_ms": int
        }
        """
        start_time = time.time()

        try:
            # Try ping endpoint first (faster)
            ping_result = self.colab_client.ping_server(colab_url)

            if ping_result.get("status") != "online":
                return {
                    "status": "offline",
                    "latency_ms": 0
                }

            # Measure full health check latency
            latency_ms = int((time.time() - start_time) * 1000)

            # Determine status based on latency
            if latency_ms < 500:
                status = "online"
            elif latency_ms < 2000:
                status = "degraded"
            else:
                status = "degraded"

            # Update cache
            server = ColabServer(
                server_id=f"server_{hash(colab_url) % 10000}",
                url=colab_url,
                status=ServerStatus(status),
                last_ping=datetime.now()
            )
            self.server_cache[colab_url] = server

            return {
                "status": status,
                "latency_ms": latency_ms
            }

        except Exception as e:
            return {
                "status": "offline",
                "latency_ms": 0
            }

    def get_server_status(self, colab_url: str) -> ColabServer:
        """Get cached or fresh server status"""
        if colab_url in self.server_cache:
            cached = self.server_cache[colab_url]
            # Return cached if less than 5 minutes old
            if cached.last_ping:
                age = (datetime.now() - cached.last_ping).total_seconds()
                if age < 300:  # 5 minutes
                    return cached

        # Fresh check
        self.health_check(colab_url)
        return self.server_cache.get(
            colab_url,
            ColabServer(
                server_id="unknown",
                url=colab_url,
                status=ServerStatus.UNKNOWN
            )
        )

    def is_server_available(self, colab_url: str, max_latency_ms: int = 2000) -> bool:
        """Check if server is available with acceptable latency"""
        result = self.health_check(colab_url)
        if result["status"] == "offline":
            return False
        if result["latency_ms"] > max_latency_ms:
            return False
        return True

    def get_all_servers_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all known servers"""
        result = {}
        for url in self.server_cache.keys():
            result[url] = self.health_check(url)
        return result

    def find_best_server(self, server_urls: list) -> str | None:
        """Find the server with lowest latency"""
        best_server = None
        best_latency = float('inf')

        for url in server_urls:
            result = self.health_check(url)
            if result["status"] != "offline" and result["latency_ms"] < best_latency:
                best_latency = result["latency_ms"]
                best_server = url

        return best_server
