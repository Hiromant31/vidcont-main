"""Prompt service for managing prompt packs."""

from typing import List, Optional, Dict, Any
from api.schemas.prompts import PromptPack, PromptPackCreate, PromptPackUpdate


class PromptService:
    """Service for managing prompt packs with in-memory storage."""
    
    def __init__(self):
        self._prompts: Dict[str, PromptPack] = {}
        self._init_default_prompts()
    
    def _init_default_prompts(self):
        """Initialize with default prompt packs."""
        defaults = [
            {"id": "story_basic", "name": "Basic Story Prompts", "type": "story", "genre": "general", "style": "narrative", "version": "1.0"},
            {"id": "character_fantasy", "name": "Fantasy Character Prompts", "type": "character", "genre": "fantasy", "style": "detailed", "version": "1.0"},
            {"id": "scene_cinematic", "name": "Cinematic Scene Prompts", "type": "scene", "genre": "general", "style": "cinematic", "version": "1.0"}
        ]
        for prompt_data in defaults:
            self._prompts[prompt_data["id"]] = PromptPack(**prompt_data)
    
    def get_all_prompts(self) -> List[PromptPack]:
        return list(self._prompts.values())
    
    def get_prompt_by_id(self, prompt_id: str) -> Optional[PromptPack]:
        return self._prompts.get(prompt_id)
    
    def create_prompt(self, data: PromptPackCreate) -> PromptPack:
        import uuid
        prompt_id = f"{data.type}_{uuid.uuid4().hex[:8]}"
        prompt = PromptPack(id=prompt_id, name=data.name, type=data.type, genre=data.genre, style=data.style, version=data.version, prompts=data.prompts, variables=data.variables)
        self._prompts[prompt_id] = prompt
        return prompt
    
    def update_prompt(self, prompt_id: str, data: PromptPackUpdate) -> Optional[PromptPack]:
        if prompt_id not in self._prompts:
            return None
        prompt = self._prompts[prompt_id]
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(prompt, key):
                setattr(prompt, key, value)
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
