"""
Channel Manager Module

Manages content channels and their configurations.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List

from .settings_schema import Channel


class ChannelManager:
    """Manages content channel configurations."""

    def __init__(self, storage: Any):
        """
        Initialize with storage interface.

        INPUT:
            storage: StorageInterface - storage for channels
        """
        self.storage = storage

    def create_channel(
        self,
        name: str,
        genre: str,
        style: str,
        settings_id: str,
        default_prompt_pack_id: Optional[str] = None
    ) -> Channel:
        """
        Creates a new channel.

        INPUT:
            name: str - channel name
            genre: str - channel genre
            style: str - channel style
            settings_id: str - associated settings ID
            default_prompt_pack_id: str | None - default prompt pack ID

        OUTPUT:
            Channel object
        """
        import uuid

        channel_id = str(uuid.uuid4())
        now = datetime.now()

        channel = Channel(
            channel_id=channel_id,
            name=name,
            genre=genre,
            style=style,
            settings_id=settings_id,
            default_prompt_pack_id=default_prompt_pack_id or ""
        )

        # Save to storage
        self.storage.save_channel(channel)

        return channel

    def get_channel(self, channel_id: str) -> Channel:
        """
        Gets channel by ID.

        INPUT:
            channel_id: str - ID of the channel

        OUTPUT:
            Channel object

        RAISES:
            ValueError if channel not found
        """
        channel = self.storage.get_channel(channel_id)

        if channel is None:
            raise ValueError(f"Channel '{channel_id}' not found")

        return channel

    def update_channel(
        self,
        channel_id: str,
        patch: Dict[str, Any]
    ) -> Channel:
        """
        Updates channel with partial data.

        INPUT:
            channel_id: str - ID of the channel to update
            patch: dict - fields to update

        OUTPUT:
            Channel object with updated values

        RAISES:
            ValueError if channel not found
        """
        # Get existing channel
        channel = self.get_channel(channel_id)

        # Apply patch
        for key, value in patch.items():
            if hasattr(channel, key):
                setattr(channel, key, value)

        # Save to storage
        self.storage.save_channel(channel)

        return channel

    def delete_channel(self, channel_id: str) -> bool:
        """
        Deletes channel by ID.

        INPUT:
            channel_id: str - ID of the channel to delete

        OUTPUT:
            bool - True if deleted, False if not found
        """
        return self.storage.delete_channel(channel_id)

    def list_channels(self, settings_id: Optional[str] = None) -> List[Channel]:
        """
        Lists all channels, optionally filtered by settings_id.

        INPUT:
            settings_id: str | None - filter by settings ID

        OUTPUT:
            list[Channel] - all matching channels
        """
        all_channels = self.storage.list_channels()

        if settings_id:
            return [ch for ch in all_channels if ch.settings_id == settings_id]

        return all_channels

    def get_channel_by_name(self, name: str) -> Optional[Channel]:
        """
        Gets channel by name.

        INPUT:
            name: str - channel name

        OUTPUT:
            Channel object or None if not found
        """
        all_channels = self.storage.list_channels()

        for channel in all_channels:
            if channel.name == name:
                return channel

        return None
