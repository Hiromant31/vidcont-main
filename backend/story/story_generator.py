"""
Story Generator Module

Generates raw story from idea using prompt templates.
Does NOT generate images, TTS, or manage pipeline.
"""
import uuid
from datetime import datetime
from typing import Dict, Any

from .story_schema import Story, GenerateStoryInput


class StoryGenerator:
    """
    Generates raw story from idea.
    
    Responsibilities:
    - Take idea + genre + style + channel_id
    - Use prompt templates to generate story
    - Return structured Story object
    
    Does NOT:
    - Generate images
    - Call TTS
    - Manage pipeline state
    """
    
    def __init__(self, prompt_manager=None):
        """
        Initialize with optional prompt manager for template retrieval.
        
        Args:
            prompt_manager: PromptManager instance for getting story generation templates
        """
        self.prompt_manager = prompt_manager
    
    def generate_story(self, input_data: Dict[str, Any]) -> Story:
        """
        Generate a story from idea.
        
        Args:
            input_data: Dict with keys:
                - idea: str
                - genre: str
                - style: str
                - channel_id: str
        
        Returns:
            Story object with generated raw_story
            
        Flow:
        1. Get story_generation prompt template from prompt_manager
        2. Render template with variables (idea, genre, style)
        3. Call LLM (external, not implemented here)
        4. Parse response and create Story object
        """
        idea = input_data["idea"]
        genre = input_data["genre"]
        style = input_data["style"]
        channel_id = input_data["channel_id"]
        
        # Generate unique story ID
        story_id = str(uuid.uuid4())
        
        # In real implementation:
        # 1. Get prompt template from prompt_manager
        # 2. Render with variables
        # 3. Call LLM API
        # 4. Parse response
        
        # Placeholder: simulate story generation
        raw_story = self._simulate_story_generation(idea, genre, style)
        
        # Extract tone from style (simplified)
        tone = self._extract_tone(style)
        
        # Default duration target (will be adapted later)
        duration_target = 60  # seconds
        
        return Story(
            story_id=story_id,
            idea=idea,
            raw_story=raw_story,
            genre=genre,
            tone=tone,
            style=style,
            duration_target=duration_target,
            created_at=datetime.now()
        )
    
    def _simulate_story_generation(self, idea: str, genre: str, style: str) -> str:
        """
        Simulate story generation (placeholder for LLM call).
        
        In production, this would:
        1. Get prompt template
        2. Render with variables
        3. Call LLM API
        4. Return generated text
        """
        # Placeholder logic
        return f"In a {genre} setting with {style} style: {idea}. " \
               f"The story unfolds with compelling characters and dramatic moments."
    
    def _extract_tone(self, style: str) -> str:
        """Extract tone from style description."""
        tone_map = {
            "dramatic": "intense",
            "comedic": "light-hearted",
            "mysterious": "suspenseful",
            "romantic": "emotional",
            "action": "exciting",
            "horror": "dark",
            "fantasy": "magical",
            "sci-fi": "futuristic"
        }
        return tone_map.get(style.lower(), "neutral")
