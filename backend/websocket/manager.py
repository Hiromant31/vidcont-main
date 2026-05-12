"""
WebSocket Manager - Realtime обновления для frontend
"""
import asyncio
import json
from typing import Dict, Set
from fastapi import WebSocket
from core.logger import setup_logger

logger = setup_logger(__name__)

class WebSocketManager:
    """Менеджер WebSocket соединений"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Подключить клиента"""
        await websocket.accept()
        # Используем job_id или user_id как ключ
        connection_id = "default"  # В реальности извлекать из query params
        if connection_id not in self.active_connections:
            self.active_connections[connection_id] = set()
        self.active_connections[connection_id].add(websocket)
        logger.info(f"WebSocket client connected: {connection_id}")
        
        # Keep connection alive with receive loop
        try:
            while True:
                # Receive messages to keep connection alive
                data = await websocket.receive_text()
                logger.debug(f"Received message from {connection_id}: {data}")
        except Exception as e:
            logger.info(f"WebSocket connection closed for {connection_id}: {e}")
        finally:
            self.disconnect(websocket, connection_id)
    
    def disconnect(self, websocket: WebSocket, connection_id: str):
        """Отключить клиента"""
        if connection_id in self.active_connections:
            self.active_connections[connection_id].remove(websocket)
            if not self.active_connections[connection_id]:
                del self.active_connections[connection_id]
        logger.info(f"WebSocket client disconnected: {connection_id}")
    
    async def send_personal_message(self, message: dict, connection_id: str):
        """Отправить сообщение конкретному клиенту"""
        if connection_id in self.active_connections:
            for connection in self.active_connections[connection_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message: {e}")
    
    async def broadcast(self, message: dict):
        """Отправить сообщение всем клиентам"""
        for connections in self.active_connections.values():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting message: {e}")
    
    async def send_job_update(self, job_id: str, status: str, progress: float, stage: str = None):
        """Отправить обновление статуса задачи"""
        message = {
            "type": "job_update",
            "job_id": job_id,
            "status": status,
            "progress": progress,
            "stage": stage
        }
        await self.send_personal_message(message, job_id)
    
    async def send_stage_complete(self, job_id: str, stage: str, output: dict = None):
        """Отправить уведомление о завершении этапа"""
        message = {
            "type": "stage_complete",
            "job_id": job_id,
            "stage": stage,
            "output": output
        }
        await self.send_personal_message(message, job_id)
    
    async def send_error(self, job_id: str, error: str, stage: str = None):
        """Отправить уведомление об ошибке"""
        message = {
            "type": "error",
            "job_id": job_id,
            "error": error,
            "stage": stage
        }
        await self.send_personal_message(message, job_id)
    
    async def send_logs(self, job_id: str, logs: list):
        """Отправить логи задачи"""
        message = {
            "type": "logs",
            "job_id": job_id,
            "logs": logs
        }
        await self.send_personal_message(message, job_id)

# Singleton instance
_manager = None

def get_websocket_manager() -> WebSocketManager:
    global _manager
    if _manager is None:
        _manager = WebSocketManager()
    return _manager
