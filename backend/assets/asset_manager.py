"""Asset Manager - управление ассетами (файлами)"""
import json
import os
import shutil
import random
from datetime import datetime, timedelta
from typing import Optional, List
from api.schemas.asset_schema import (
    AssetResponse, AssetUsageResponse, AssetType, AssetStatus,
    AssetEntityType
)


class AssetManager:
    """Менеджер для хранения и управления ассетами."""

    def __init__(self, storage_path: str = "./storage/assets"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        self._index_path = os.path.join(storage_path, "index.json")
        self._ensure_index()

    def _ensure_index(self):
        if not os.path.exists(self._index_path):
            self._save_index([])
            self._seed_mock_assets()

    def _load_index(self) -> list:
        if not os.path.exists(self._index_path):
            return []
        with open(self._index_path, "r") as f:
            return json.load(f)

    def _save_index(self, assets: list):
        with open(self._index_path, "w") as f:
            json.dump(assets, f, indent=2, default=str)

    def _seed_mock_assets(self):
        """Создать тестовые ассеты для демо."""
        now = datetime.utcnow()
        mock_assets = []
        types = ["image", "audio", "video", "subtitle", "thumbnail"]
        statuses = ["ready", "ready", "ready", "processing", "failed"]
        for i in range(12):
            asset_type = types[i % len(types)]
            mock_assets.append({
                "id": f"asset_{i+1:03d}",
                "project_id": f"proj_{random.randint(1,5):03d}",
                "job_id": f"job_{random.randint(1,20):03d}",
                "scene_id": f"scene_{random.randint(1,10):03d}" if random.random() > 0.5 else None,
                "render_id": f"render_{random.randint(1,8):03d}" if asset_type == "video" else None,
                "type": asset_type,
                "url": f"/static/assets/{asset_type}_{i+1:03d}.{'mp4' if asset_type == 'video' else 'mp3' if asset_type == 'audio' else 'png' if asset_type in ('image','thumbnail') else 'srt'}",
                "thumbnail_url": f"/static/assets/thumb_{i+1:03d}.png" if asset_type in ("video", "image") else None,
                "status": statuses[i % len(statuses)],
                "metadata": {"source": "mock", "original_name": f"mock_{asset_type}_{i+1:03d}"},
                "size_bytes": random.randint(10000, 5000000),
                "duration_sec": round(random.uniform(5.0, 120.0), 1) if asset_type in ("video", "audio") else None,
                "created_at": (now - timedelta(hours=random.randint(1, 168))).isoformat(),
                "name": f"Mock {asset_type.title()} {i+1:03d}"
            })
        self._save_index(mock_assets)

    def get_all(self, asset_type: Optional[str] = None,
                status: Optional[str] = None,
                search: Optional[str] = None) -> List[AssetResponse]:
        """Получить список ассетов с фильтрацией."""
        assets = self._load_index()
        if asset_type and asset_type != "all":
            assets = [a for a in assets if a["type"] == asset_type]
        if status and status != "all":
            assets = [a for a in assets if a["status"] == status]
        if search:
            search_lower = search.lower()
            assets = [a for a in assets
                      if (a.get("name") and search_lower in a["name"].lower())
                      or search_lower in a["id"].lower()]
        return [AssetResponse(**a) for a in assets]

    def get_by_id(self, asset_id: str) -> Optional[AssetResponse]:
        """Получить ассет по ID."""
        assets = self._load_index()
        for a in assets:
            if a["id"] == asset_id:
                return AssetResponse(**a)
        return None

    def delete(self, asset_id: str) -> bool:
        """Удалить ассет."""
        assets = self._load_index()
        filtered = [a for a in assets if a["id"] != asset_id]
        if len(filtered) == len(assets):
            return False
        self._save_index(filtered)
        return True

    def reuse(self, asset_id: str, target_entity: dict) -> Optional[AssetResponse]:
        """Переиспользовать ассет (создать ссылку на него)."""
        asset = self.get_by_id(asset_id)
        if not asset:
            return None
        # В реальном приложении здесь создаётся запись в БД
        return asset

    def get_usage(self, asset_id: str) -> List[AssetUsageResponse]:
        """История использования ассета."""
        # Mock данные
        now = datetime.utcnow()
        return [
            AssetUsageResponse(
                id=f"usage_{asset_id}_1",
                asset_id=asset_id,
                entity_type=AssetEntityType.scene,
                entity_id=f"scene_{random.randint(1,10):03d}",
                used_at=(now - timedelta(hours=random.randint(1, 72))).isoformat(),
                context="Used as background"
            ),
            AssetUsageResponse(
                id=f"usage_{asset_id}_2",
                asset_id=asset_id,
                entity_type=AssetEntityType.job,
                entity_id=f"job_{random.randint(1,20):03d}",
                used_at=(now - timedelta(hours=random.randint(1, 72))).isoformat(),
                context="Generated asset"
            )
        ]

    def get_download_path(self, asset_id: str) -> Optional[str]:
        """Получить путь к файлу для скачивания."""
        asset = self.get_by_id(asset_id)
        if not asset:
            return None
        # В реальном приложении возвращать реальный путь к файлу
        return asset.url
