"""
Consistency Manager Module
Manages character identity locking and applies consistency to scene prompts.
"""
from typing import Dict, Any, List
from .character_schema import Character, ReferenceImage


class ConsistencyManager:
    """
    Manages character identity consistency across all generated scenes.
    Locks character identities using reference images and ensures
    they are applied consistently in all scene generations.
    """

    def __init__(self):
        # In-memory store for locked identities
        # Format: {character_id: {"reference": ReferenceImage, "locked": bool}}
        self._locked_identities: Dict[str, Dict[str, Any]] = {}

    def lock_character_identity(self, character_id: str,
                                 reference_image: ReferenceImage) -> Dict[str, str]:
        """
        Lock a character's identity using a reference image.
        
        Args:
            character_id: ID of the character to lock
            reference_image: Reference image to use for consistency
            
        Returns:
            Status dictionary
            
        Effect:
            Once locked, all scene generations for this character
            must use this reference to maintain visual consistency.
        """
        self._locked_identities[character_id] = {
            "reference": reference_image,
            "locked": True,
            "seed": reference_image.seed
        }
        
        return {"status": "locked"}

    def apply_consistency(self, character_id: str,
                          scene_prompt: str) -> Dict[str, str]:
        """
        Apply character consistency to a scene prompt.
        
        Args:
            character_id: ID of the character
            scene_prompt: The original scene prompt
            
        Returns:
            Modified prompt with consistency markers
            
        Behavior:
            - If character is locked, inject reference info
            - Add consistency enforcement instructions
            - Ensure seed is used for generation
        """
        if character_id not in self._locked_identities:
            return {"modified_prompt": scene_prompt}
        
        identity = self._locked_identities[character_id]
        reference = identity["reference"]
        
        # Build consistency injection
        consistency_injection = (
            f"\n\nCONSISTENCY REQUIREMENTS:\n"
            f"- Character ID: {character_id}\n"
            f"- Reference Seed: {reference.seed}\n"
            f"- Reference URL: {reference.image_url}\n"
            f"- Style Locked: {reference.style_locked}\n"
            f"- INSTRUCTION: Use exact same facial features, body type, "
            f"clothing, and proportions as reference image.\n"
            f"- DO NOT alter character appearance in any way."
        )
        
        modified_prompt = scene_prompt + consistency_injection
        
        return {"modified_prompt": modified_prompt}

    def get_locked_characters(self) -> List[str]:
        """Get list of all locked character IDs."""
        return list(self._locked_identities.keys())

    def is_character_locked(self, character_id: str) -> bool:
        """Check if a character identity is locked."""
        return character_id in self._locked_identities

    def get_reference_seed(self, character_id: str) -> str:
        """Get the reference seed for a locked character."""
        if character_id in self._locked_identities:
            return self._locked_identities[character_id]["seed"]
        return None

    def unlock_character(self, character_id: str) -> Dict[str, str]:
        """Unlock a character's identity."""
        if character_id in self._locked_identities:
            del self._locked_identities[character_id]
            return {"status": "unlocked"}
        return {"status": "not_found"}

    def clear_all_locks(self) -> Dict[str, str]:
        """Clear all character locks."""
        self._locked_identities.clear()
        return {"status": "cleared"}
