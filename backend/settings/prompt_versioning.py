"""
Prompt Versioning Module

Manages prompt template versions.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional

from .settings_schema import PromptTemplate


class PromptVersioning:
    """Manages versioning of prompt templates."""

    def __init__(self, storage: Any):
        """
        Initialize with storage interface.

        INPUT:
            storage: StorageInterface - storage for prompt templates
        """
        self.storage = storage

    def get_latest_version(self, template_id: str) -> PromptTemplate:
        """
        Gets the latest version of a prompt template.

        INPUT:
            template_id: str - ID of the template

        OUTPUT:
            PromptTemplate with the highest version number

        RAISES:
            ValueError if template not found
        """
        # Get all versions of this template
        all_versions = self._get_all_versions(template_id)

        if not all_versions:
            raise ValueError(f"Template '{template_id}' not found")

        # Return the one with highest version
        return max(all_versions, key=lambda t: t.version)

    def create_new_version(
        self,
        template_id: str,
        new_content: str
    ) -> PromptTemplate:
        """
        Creates a new version of an existing template.

        INPUT:
            template_id: str - ID of the template to version
            new_content: str - new content for the template

        OUTPUT:
            PromptTemplate with incremented version number

        RAISES:
            ValueError if original template not found
        """
        # Get the latest version
        latest = self.get_latest_version(template_id)

        # Create new version
        new_version = PromptTemplate(
            template_id=latest.template_id,
            name=latest.name,
            stage=latest.stage,
            content=new_content,
            variables=latest.variables,
            version=latest.version + 1,
            channel_id=latest.channel_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Save to storage
        self.storage.save_prompt_template(new_version)

        return new_version

    def _get_all_versions(self, template_id: str) -> List[PromptTemplate]:
        """Gets all versions of a template."""
        # This would call storage to get all versions
        # For now, assume storage has a method to get by template_id
        try:
            return self.storage.get_prompt_templates_by_id(template_id)
        except (AttributeError, NotImplementedError):
            # Fallback if storage doesn't have this method
            return []

    def get_version_history(
        self,
        template_id: str
    ) -> List[Dict[str, Any]]:
        """
        Gets version history for a template.

        INPUT:
            template_id: str - ID of the template

        OUTPUT:
            list of dicts with version info:
            [
                {
                    "version": int,
                    "created_at": datetime,
                    "content_preview": str
                },
                ...
            ]
        """
        all_versions = self._get_all_versions(template_id)

        history = []
        for template in sorted(all_versions, key=lambda t: t.version):
            history.append({
                "version": template.version,
                "created_at": template.created_at,
                "content_preview": template.content[:100] + "..." if len(template.content) > 100 else template.content
            })

        return history
