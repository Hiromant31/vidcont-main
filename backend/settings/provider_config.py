"""
Provider Config Module

Manages AI provider configurations.
"""

from typing import Optional, Dict, Any

from .settings_schema import Settings, ProviderConfig


class ProviderConfigManager:
    """Manages AI provider configurations."""

    # Provider base URLs
    PROVIDER_URLS = {
        "openai": "https://api.openai.com/v1",
        "yandex": "https://llm.api.cloud.yandex.net/foundationModels/v1",
        "other": ""
    }

    def get_provider_config(self, settings: Settings) -> ProviderConfig:
        """
        Gets provider configuration from settings.

        INPUT:
            settings: Settings - settings object with provider info

        OUTPUT:
            ProviderConfig with provider details
        """
        base_url = self.PROVIDER_URLS.get(
            settings.ai_provider,
            self.PROVIDER_URLS["other"]
        )

        return ProviderConfig(
            provider_name=settings.ai_provider,
            api_key=settings.api_key,
            base_url=base_url,
            model=settings.model,
            folder_id=settings.folder_id
        )

    def validate_provider(self, settings: Settings) -> bool:
        """
        Validates that the provider configuration is complete.

        INPUT:
            settings: Settings - settings to validate

        OUTPUT:
            bool - True if valid, False otherwise
        """
        if not settings.api_key:
            return False

        if settings.ai_provider not in self.PROVIDER_URLS:
            return False

        if not settings.model:
            return False

        return True
