"""
Character Builder Module
Builds detailed visual prompts for characters based on style profiles.
"""
from typing import Dict, Any
from .character_schema import Character, StyleProfile


class CharacterBuilder:
    """
    Builds comprehensive visual prompts for characters.
    Combines character description with style profile for consistency.
    """

    def build_character_prompt(self, character: Character, 
                                style_profile: StyleProfile) -> Dict[str, str]:
        """
        Build a detailed visual prompt for a character.
        
        Args:
            character: The character to build prompt for
            style_profile: The style profile to apply
            
        Returns:
            Dictionary containing the generated prompt
            
        Prompt includes:
            - Appearance details
            - Clothing
            - Age/type
            - Atmosphere
            - Style from StyleProfile
        """
        # Build base description
        base_prompt = self._build_base_description(character)
        
        # Add style elements
        styled_prompt = self._apply_style(base_prompt, style_profile)
        
        # Add consistency markers
        final_prompt = self._add_consistency_markers(styled_prompt, character)
        
        return {"prompt": final_prompt}

    def _build_base_description(self, character: Character) -> str:
        """Build base character description."""
        parts = [
            f"Character: {character.name}",
            f"Type: {character.type}",
            f"Role: {character.role}",
            f"Description: {character.description}"
        ]
        return ". ".join(parts)

    def _apply_style(self, prompt: str, style_profile: StyleProfile) -> str:
        """Apply style profile to the character prompt."""
        style_elements = [
            prompt,
            f"Visual Style: {style_profile.visual_style}",
            f"Mood: {style_profile.mood}",
            f"Lighting: {style_profile.lighting}",
            f"Color Palette: {style_profile.color_palette}",
            f"Cinematic Rules: {style_profile.cinematic_rules}"
        ]
        return ". ".join(style_elements)

    def _add_consistency_markers(self, prompt: str, character: Character) -> str:
        """Add consistency markers to ensure visual stability."""
        markers = [
            prompt,
            f"CONSISTENCY_TAG: {character.consistency_tag}",
            "MAINTAIN: Same facial features, body type, and clothing across all shots",
            "REFERENCE: Use this exact appearance in every scene"
        ]
        return ". ".join(markers)
