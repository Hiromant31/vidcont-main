"""
Settings Manager Module

Manages AI provider and pipeline settings.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from .settings_schema import Settings


class SettingsManager:
    """Manages AI provider and pipeline configuration settings."""

    def __init__(self, storage: Any):
        """
        Initialize with storage interface.

        INPUT:
            storage: StorageInterface - storage for settings
        """
        self.storage = storage

    def get_settings(self, settings_id: str) -> Settings:
        """
        Gets settings by ID.

        INPUT:
            settings_id: str - ID of the settings

        OUTPUT:
            Settings object

        RAISES:
            ValueError if settings not found
        """
        settings = self.storage.get_settings(settings_id)

        if settings is None:
            raise ValueError(f"Settings '{settings_id}' not found")

        return settings

    def update_settings(
        self,
        settings_id: str,
        patch: Dict[str, Any]
    ) -> Settings:
        """
        Updates settings with partial data.

        INPUT:
            settings_id: str - ID of the settings to update
            patch: dict - fields to update

        OUTPUT:
            Settings object with updated values

        RAISES:
            ValueError if settings not found
        """
        # Get existing settings
        settings = self.get_settings(settings_id)

        # Apply patch
        for key, value in patch.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        # Update timestamp
        settings.updated_at = datetime.now()

        # Save to storage
        self.storage.save_settings(settings)

        return settings

    def create_settings(
        self,
        settings_id: str,
        ai_provider: str,
        model: str,
        api_key: str,
        folder_id: Optional[str],
        default_quality: str,
        auto_continue_pipeline: bool
    ) -> Settings:
        """
        Creates new settings.

        INPUT:
            settings_id: str - unique ID for settings
            ai_provider: str - "openai" | "yandex" | "other"
            model: str - model name
            api_key: str - API key
            folder_id: str | None - Yandex folder ID if applicable
            default_quality: str - "240" | "360" | "480" | "720" | "1080"
            auto_continue_pipeline: bool - whether to auto-continue pipeline

        OUTPUT:
            Settings object
        """
        now = datetime.now()

        settings = Settings(
            settings_id=settings_id,
            ai_provider=ai_provider,
            model=model,
            api_key=api_key,
            folder_id=folder_id,
            default_quality=default_quality,
            auto_continue_pipeline=auto_continue_pipeline,
            created_at=now,
            updated_at=now
        )

        # Save to storage
        self.storage.save_settings(settings)

        return settings

    def delete_settings(self, settings_id: str) -> bool:
        """
        Deletes settings by ID.

        INPUT:
            settings_id: str - ID of the settings to delete

        OUTPUT:
            bool - True if deleted, False if not found
        """
        return self.storage.delete_settings(settings_id)

    def list_settings(self) -> list:
        """
        Lists all available settings.

        OUTPUT:
            list[Settings] - all settings
        """
        return self.storage.list_settings()
