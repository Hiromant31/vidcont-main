"""
Prompt Builder Module
Combines character and scene information into final generation prompts.
"""
from typing import Dict, Any, List
from .character_schema import Character, StyleProfile, ReferenceImage


class PromptBuilder:
    """
    Builds final prompts for image generation by combining
    character data, style profiles, and scene context.
    """

    def build_scene_prompt(self, scene_description: str,
                           characters: List[Character],
                           style_profile: StyleProfile,
                           reference_images: List[ReferenceImage] = None) -> Dict[str, str]:
        """
        Build a complete prompt for scene generation.
        
        Args:
            scene_description: Description of the scene
            characters: Characters present in the scene
            style_profile: Style profile to apply
            reference_images: Optional reference images for consistency
            
        Returns:
            Dictionary containing the complete generation prompt
        """
        # Start with scene description
        prompt_parts = [f"Scene: {scene_description}"]
        
        # Add style information
        prompt_parts.append(f"Style: {style_profile.visual_style}")
        prompt_parts.append(f"Mood: {style_profile.mood}")
        prompt_parts.append(f"Lighting: {style_profile.lighting}")
        prompt_parts.append(f"Colors: {style_profile.color_palette}")
        
        # Add character information with consistency markers
        if characters:
            char_prompts = []
            for char in characters:
                char_info = f"Character: {char.name} ({char.type}, {char.role})"
                if char.visual_prompt:
                    char_info += f" - {char.visual_prompt}"
                if reference_images:
                    refs = [r for r in reference_images if r.character_id == char.character_id]
                    if refs:
                        char_info += f" [REFERENCE_LOCKED: seed={refs[0].seed}]"
                char_prompts.append(char_info)
            prompt_parts.append("Characters: " + "; ".join(char_prompts))
        
        # Add consistency rules
        prompt_parts.append(style_profile.cinematic_rules)
        
        # Add technical requirements
        prompt_parts.append("TECHNICAL: High quality, consistent character appearance, cinematic composition")
        
        return {"prompt": ". ".join(prompt_parts)}

    def build_character_insertion_prompt(self, character: Character,
                                          style_profile: StyleProfile,
                                          action: str) -> Dict[str, str]:
        """
        Build a prompt for inserting a character into a specific action.
        
        Args:
            character: The character to insert
            style_profile: Style profile
            action: The action the character is performing
            
        Returns:
            Dictionary containing the insertion prompt
        """
        prompt_parts = [
            f"Character: {character.name}",
            f"Action: {action}",
            f"Description: {character.description}",
            f"Style: {style_profile.visual_style}",
            f"Mood: {style_profile.mood}",
            f"CONSISTENCY_TAG: {character.consistency_tag}",
            "MAINTAIN: Exact same appearance as reference"
        ]
        
        return {"prompt": ". ".join(prompt_parts)}
