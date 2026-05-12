"""
Prompt Manager Module

Manages prompt templates and prompt packs.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List

from .settings_schema import PromptTemplate, PromptPack


class PromptManager:
    """Manages prompt templates and prompt packs."""

    def __init__(self, storage: Any):
        """
        Initialize with storage interface.

        INPUT:
            storage: StorageInterface - storage for prompts
        """
        self.storage = storage

    def get_prompt_pack(self, channel_id: str) -> PromptPack:
        """
        Gets the prompt pack for a channel.

        INPUT:
            channel_id: str - ID of the channel

        OUTPUT:
            PromptPack object

        RAISES:
            ValueError if prompt pack not found
        """
        prompt_pack = self.storage.get_prompt_pack(channel_id)

        if prompt_pack is None:
            raise ValueError(f"Prompt pack for channel '{channel_id}' not found")

        return prompt_pack

    def get_prompt_template(self, template_id: str) -> PromptTemplate:
        """
        Gets a prompt template by ID.

        INPUT:
            template_id: str - ID of the template

        OUTPUT:
            PromptTemplate object

        RAISES:
            ValueError if template not found
        """
        template = self.storage.get_prompt_template(template_id)

        if template is None:
            raise ValueError(f"Prompt template '{template_id}' not found")

        return template

    def create_prompt_template(
        self,
        name: str,
        stage: str,
        content: str,
        variables: List[str],
        channel_id: str,
        version: int = 1
    ) -> PromptTemplate:
        """
        Creates a new prompt template.

        INPUT:
            name: str - template name
            stage: str - stage this template is for
            content: str - template content with {{variable}} placeholders
            variables: list[str] - list of variable names used in template
            channel_id: str - associated channel ID
            version: int - version number (default: 1)

        OUTPUT:
            PromptTemplate object
        """
        import uuid

        template_id = str(uuid.uuid4())
        now = datetime.now()

        template = PromptTemplate(
            template_id=template_id,
            name=name,
            stage=stage,
            content=content,
            variables=variables,
            version=version,
            channel_id=channel_id,
            created_at=now,
            updated_at=now
        )

        # Save to storage
        self.storage.save_prompt_template(template)

        return template

    def update_prompt_template(
        self,
        template_id: str,
        patch: Dict[str, Any]
    ) -> PromptTemplate:
        """
        Updates a prompt template with partial data.

        INPUT:
            template_id: str - ID of the template to update
            patch: dict - fields to update

        OUTPUT:
            PromptTemplate object with updated values

        RAISES:
            ValueError if template not found
        """
        # Get existing template
        template = self.get_prompt_template(template_id)

        # Apply patch
        for key, value in patch.items():
            if hasattr(template, key):
                setattr(template, key, value)

        # Update timestamp
        template.updated_at = datetime.now()

        # Save to storage
        self.storage.save_prompt_template(template)

        return template

    def delete_prompt_template(self, template_id: str) -> bool:
        """
        Deletes a prompt template by ID.

        INPUT:
            template_id: str - ID of the template to delete

        OUTPUT:
            bool - True if deleted, False if not found
        """
        return self.storage.delete_prompt_template(template_id)

    def create_prompt_pack(
        self,
        channel_id: str,
        story_prompt_id: str,
        character_prompt_id: str,
        scene_prompt_id: str,
        storyboard_prompt_id: str,
        metadata_prompt_id: str
    ) -> PromptPack:
        """
        Creates a new prompt pack.

        INPUT:
            channel_id: str - associated channel ID
            story_prompt_id: str - template ID for story generation
            character_prompt_id: str - template ID for character extraction
            scene_prompt_id: str - template ID for scene generation
            storyboard_prompt_id: str - template ID for storyboard generation
            metadata_prompt_id: str - template ID for metadata generation

        OUTPUT:
            PromptPack object
        """
        import uuid

        pack_id = str(uuid.uuid4())

        pack = PromptPack(
            pack_id=pack_id,
            channel_id=channel_id,
            story_prompt_id=story_prompt_id,
            character_prompt_id=character_prompt_id,
            scene_prompt_id=scene_prompt_id,
            storyboard_prompt_id=storyboard_prompt_id,
            metadata_prompt_id=metadata_prompt_id
        )

        # Save to storage
        self.storage.save_prompt_pack(pack)

        return pack

    def update_prompt_pack(
        self,
        pack_id: str,
        patch: Dict[str, Any]
    ) -> PromptPack:
        """
        Updates a prompt pack with partial data.

        INPUT:
            pack_id: str - ID of the pack to update
            patch: dict - fields to update

        OUTPUT:
            PromptPack object with updated values

        RAISES:
            ValueError if pack not found
        """
        # Get existing pack
        pack = self.storage.get_prompt_pack_by_id(pack_id)

        if pack is None:
            raise ValueError(f"Prompt pack '{pack_id}' not found")

        # Apply patch
        for key, value in patch.items():
            if hasattr(pack, key):
                setattr(pack, key, value)

        # Save to storage
        self.storage.save_prompt_pack(pack)

        return pack

    def delete_prompt_pack(self, pack_id: str) -> bool:
        """
        Deletes a prompt pack by ID.

        INPUT:
            pack_id: str - ID of the pack to delete

        OUTPUT:
            bool - True if deleted, False if not found
        """
        return self.storage.delete_prompt_pack(pack_id)

    def get_templates_by_stage(
        self,
        channel_id: str,
        stage: str
    ) -> List[PromptTemplate]:
        """
        Gets all templates for a specific stage and channel.

        INPUT:
            channel_id: str - channel ID
            stage: str - stage name

        OUTPUT:
            list[PromptTemplate] - matching templates
        """
        all_templates = self.storage.list_prompt_templates(channel_id)

        return [t for t in all_templates if t.stage == stage]
