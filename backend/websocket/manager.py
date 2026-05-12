"""
WebSocket Manager - Realtime обновления для frontend
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, Set, Optional
from fastapi import WebSocket
from core.logger import setup_logger

logger = setup_logger(__name__)

class WebSocketManager:
    """Менеджер WebSocket соединений — единый стандарт событий."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        connection_id = "default"
        if connection_id not in self.active_connections:
            self.active_connections[connection_id] = set()
        self.active_connections[connection_id].add(websocket)
        logger.info(f"WebSocket client connected: {connection_id}")
        try:
            while True:
                data = await websocket.receive_text()
                logger.debug(f"Received: {data}")
        except Exception as e:
            logger.info(f"WebSocket closed for {connection_id}: {e}")
        finally:
            self.disconnect(websocket, connection_id)

    def disconnect(self, websocket: WebSocket, connection_id: str):
        if connection_id in self.active_connections:
            self.active_connections[connection_id].remove(websocket)
            if not self.active_connections[connection_id]:
                del self.active_connections[connection_id]
        logger.info(f"WebSocket client disconnected: {connection_id}")

    async def _send(self, message: dict, connection_id: Optional[str] = None):
        """Внутренний метод отправки сообщения."""
        if connection_id:
            if connection_id in self.active_connections:
                for conn in self.active_connections[connection_id]:
                    try:
                        await conn.send_json(message)
                    except Exception as e:
                        logger.error(f"Send error: {e}")
        else:
            for connections in self.active_connections.values():
                for conn in connections:
                    try:
                        await conn.send_json(message)
                    except Exception as e:
                        logger.error(f"Broadcast error: {e}")

    async def send_event(self, event_type: str, data: dict, connection_id: Optional[str] = None):
        """Отправить событие в едином формате { type, data, timestamp }."""
        message = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self._send(message, connection_id)

    # --- Job события ---

    async def send_job_started(self, job_id: str, project_id: str):
        await self.send_event("job_started", {
            "job_id": job_id,
            "project_id": project_id,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat()
        })

    async def send_job_progress(self, job_id: str, progress: float, current_stage: Optional[str] = None):
        await self.send_event("job_progress", {
            "job_id": job_id,
            "progress": progress,
            "current_stage": current_stage
        })

    async def send_job_completed(self, job_id: str, result: Optional[dict] = None):
        await self.send_event("job_completed", {
            "job_id": job_id,
            "result": result
        })

    async def send_job_failed(self, job_id: str, error: str, stage: Optional[str] = None):
        await self.send_event("job_failed", {
            "job_id": job_id,
            "error": error,
            "stage": stage
        })

    # --- Pipeline события ---

    async def send_stage_completed(self, job_id: str, stage_name: str, output: Optional[dict] = None):
        await self.send_event("stage_completed", {
            "job_id": job_id,
            "stage_name": stage_name,
            "output": output
        })

    async def send_stage_failed(self, job_id: str, stage_name: str, error: str):
        await self.send_event("stage_failed", {
            "job_id": job_id,
            "stage_name": stage_name,
            "error": error
        })

    # --- Render события ---

    async def send_render_started(self, render_job_id: str, job_id: str):
        await self.send_event("render_started", {
            "render_job_id": render_job_id,
            "job_id": job_id,
            "status": "uploading"
        })

    async def send_render_completed(self, render_job_id: str, video_url: str):
        await self.send_event("render_completed", {
            "render_job_id": render_job_id,
            "video_url": video_url
        })

    # --- Logs ---

    async def send_logs_updated(self, job_id: str, logs: list):
        await self.send_event("logs_updated", {
            "job_id": job_id,
            "logs": logs
        })

    # --- Metrics ---

    async def send_metrics_updated(self, cpu: float, memory: float,
                                    connections: int, queue_size: int,
                                    throughput: float):
        await self.send_event("metrics_updated", {
            "cpu_usage": cpu,
            "memory_usage": memory,
            "active_connections": connections,
            "queue_size": queue_size,
            "throughput_per_min": throughput
        })

    async def send_error_spike_detected(self, metric: str, value: float,
                                         threshold: float, message: str):
        await self.send_event("error_spike_detected", {
            "metric": metric,
            "value": value,
            "threshold": threshold,
            "message": message
        })

    # --- Asset события ---

    async def send_asset_created(self, asset_data: dict):
        await self.send_event("asset_created", asset_data)

    async def send_asset_updated(self, asset_data: dict):
        await self.send_event("asset_updated", asset_data)

    async def send_asset_deleted(self, asset_id: str):
        await self.send_event("asset_deleted", {"asset_id": asset_id})

    async def send_asset_ready(self, asset_data: dict):
        await self.send_event("asset_ready", asset_data)

    async def send_asset_failed(self, asset_id: str, error: str):
        await self.send_event("asset_failed", {"asset_id": asset_id, "error": error})


# Singleton instance
_manager = None

def get_websocket_manager() -> WebSocketManager:
    global _manager
    if _manager is None:
        _manager = WebSocketManager()
    return _manager
