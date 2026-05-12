"""App Settings Manager for the modular settings module."""
import json
import os
from datetime import datetime
from typing import Optional
from api.schemas.app_settings_schema import AppSettingsRequest


class AppSettingsManager:
    """Manages application-level settings (AI, TTS, Render, Colab, Pipeline)."""

    def __init__(self, storage_path: str = "./storage/settings.json"):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            self._save_defaults()

    def _save_defaults(self):
        defaults = AppSettingsRequest().model_dump()
        with open(self.storage_path, "w") as f:
            json.dump(defaults, f, indent=2)

    def get_settings(self) -> dict:
        if not os.path.exists(self.storage_path):
            self._save_defaults()
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def update_settings(self, patch: dict) -> dict:
        current = self.get_settings()
        for section, values in patch.items():
            if section in current and isinstance(values, dict):
                current[section].update(values)
            else:
                current[section] = values
        with open(self.storage_path, "w") as f:
            json.dump(current, f, indent=2)
        return current

    def test_connection(self) -> dict:
        """Mock: test connection to AI provider."""
        import random
        return {
            "success": True,
            "message": "Connection successful",
            "latency_ms": random.randint(50, 500)
        }

    def get_available_models(self, provider: str) -> dict:
        """Mock: return available models for a provider."""
        models = {
            "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            "yandex": ["yandexgpt", "yandexgpt-lite"],
            "anthropic": ["claude-3-opus", "claude-3-sonnet"],
            "google": ["gemini-pro", "gemini-ultra"],
            "openrouter": ["openai/gpt-4", "anthropic/claude-3"],
            "custom": ["custom-model"],
        }
        return {"models": models.get(provider, ["unknown"])}
