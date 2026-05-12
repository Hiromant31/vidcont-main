"""
Character Extractor Module
Analyzes story text to identify and extract characters (max 3).
"""
import uuid
from typing import List, Dict, Any
from .character_schema import Character, CharacterSet


class CharacterExtractor:
    """
    Extracts characters from story text.
    Enforces maximum 3 characters rule.
    Merges similar characters and handles groups as single entities.
    """

    def __init__(self):
        self.max_characters = 3

    def extract_characters(self, story: str, max_characters: int = 3) -> CharacterSet:
        """
        Extract characters from story text.
        
        Args:
            story: The raw story text
            max_characters: Maximum number of characters to extract (default 3)
            
        Returns:
            CharacterSet containing extracted characters
            
        Rules:
            - Merge similar characters
            - Count groups as 1 entity
            - Avoid duplicate roles
        """
        self.max_characters = max_characters
        
        # Analyze story to find character mentions
        # In production, this would use LLM to parse the story
        character_candidates = self._analyze_story(story)
        
        # Filter and merge to respect max count
        filtered_characters = self._filter_and_merge(character_candidates, max_characters)
        
        # Build final character objects
        characters = []
        for idx, char_data in enumerate(filtered_characters[:max_characters]):
            character = Character(
                character_id=str(uuid.uuid4()),
                story_id="",  # Will be set by caller
                name=char_data["name"],
                type=char_data["type"],
                description=char_data["description"],
                visual_prompt="",  # Will be built by CharacterBuilder
                role=char_data["role"],
                consistency_tag=f"char_{idx + 1}"
            )
            characters.append(character)
        
        return CharacterSet(
            set_id=str(uuid.uuid4()),
            story_id="",  # Will be set by caller
            characters=characters,
            max_count=max_characters
        )

    def _analyze_story(self, story: str) -> List[Dict[str, Any]]:
        """
        Analyze story text to identify potential characters.
        This is a placeholder - in production would use LLM.
        """
        # Placeholder implementation
        # Real implementation would parse story with LLM
        candidates = []
        
        # Simple heuristic: look for names and descriptions
        # This is intentionally basic - real version uses AI
        lines = story.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['named', 'called', 'was a', 'were a']):
                candidates.append({
                    "name": "Unknown Character",
                    "type": "human",
                    "description": line.strip(),
                    "role": "main"
                })
        
        # If no characters found, create a default based on story context
        if not candidates:
            candidates.append({
                "name": "Protagonist",
                "type": "human",
                "description": "Main character from the story",
                "role": "main"
            })
        
        return candidates

    def _filter_and_merge(self, candidates: List[Dict[str, Any]], 
                          max_count: int) -> List[Dict[str, Any]]:
        """
        Filter and merge similar characters to respect max count.
        """
        if len(candidates) <= max_count:
            return candidates
        
        # Merge logic: combine similar characters
        # Priority: main > secondary > background
        merged = []
        main_chars = [c for c in candidates if c["role"] == "main"]
        secondary_chars = [c for c in candidates if c["role"] == "secondary"]
        background_chars = [c for c in candidates if c["role"] == "background"]
        
        # Keep main characters first
        merged.extend(main_chars[:2])  # Max 2 main
        
        # Add secondary if space
        remaining = max_count - len(merged)
        if remaining > 0 and secondary_chars:
            merged.extend(secondary_chars[:remaining])
        
        # If still need more, merge others into "group"
        remaining = max_count - len(merged)
        if remaining > 0:
            others = background_chars + secondary_chars[len(merged):]
            if others:
                merged.append({
                    "name": "Supporting Characters",
                    "type": "group",
                    "description": "Additional characters in the story",
                    "role": "background"
                })
        
        return merged[:max_count]
