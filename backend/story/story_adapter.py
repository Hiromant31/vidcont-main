"""
Story Adapter Module

Adapts raw story to specific duration (e.g., 60 seconds).
Optimizes text for voiceover and video pacing.
"""
import uuid
from typing import Dict, Any, Optional

from .story_schema import Story, AdaptedStory, AdaptStoryInput, STORY_TOO_LONG_ERROR


class StoryAdapter:
    """
    Adapts story to target duration.
    
    Responsibilities:
    - Take raw story and target duration
    - Condense or expand text to fit duration
    - Optimize for voiceover pacing
    - Return AdaptedStory with voiceover script
    
    Does NOT:
    - Generate images
    - Call TTS
    - Manage pipeline state
    """
    
    # Average speaking rate: ~150 words per minute
    # For 60 seconds: ~150 words = ~25-30 seconds of actual speech
    # Accounting for pauses and pacing: ~130-140 words for 60s video
    WORDS_PER_SECOND = 2.2  # Conservative estimate for clear speech
    
    def __init__(self, llm_client=None):
        """
        Initialize with optional LLM client for text adaptation.
        
        Args:
            llm_client: LLM client for rewriting/condensing text
        """
        self.llm_client = llm_client
    
    def adapt_story_to_duration(self, input_data: Dict[str, Any]) -> AdaptedStory:
        """
        Adapt story to target duration.
        
        Args:
            input_data: Dict with keys:
                - story_id: str
                - target_duration_sec: int
        
        Returns:
            AdaptedStory with adapted_text and voiceover_script
            
        Behavior:
        - Shortens or expands text to fit duration
        - Removes unnecessary details
        - Optimizes for video dynamics
        - Creates voiceover-ready script
        """
        story_id = input_data["story_id"]
        target_duration_sec = input_data["target_duration_sec"]
        
        # In real implementation:
        # 1. Fetch Story from storage using story_id
        # 2. Get adaptation prompt template
        # 3. Render with story text + target duration
        # 4. Call LLM to adapt
        # 5. Parse response
        
        # Placeholder: simulate adaptation
        # Assume we have the raw story (would be fetched from DB)
        raw_story = self._fetch_story(story_id)
        
        # Calculate target word count
        target_words = int(target_duration_sec * self.WORDS_PER_SECOND)
        
        # Check if story is too long
        current_words = len(raw_story.split())
        if current_words > target_words * 2:  # More than 2x target
            # Would trigger force_adapt in real implementation
            pass
        
        # Adapt the story
        adapted_text = self._adapt_text(raw_story, target_words)
        
        # Create voiceover script (cleaned up version)
        voiceover_script = self._create_voiceover_script(adapted_text)
        
        # Estimate actual duration
        estimated_duration = len(voiceover_script.split()) / self.WORDS_PER_SECOND
        
        # Estimate scene count (roughly 1 scene per 10-15 seconds)
        scene_count = max(3, int(target_duration_sec / 12))
        
        return AdaptedStory(
            story_id=story_id,
            adapted_text=adapted_text,
            voiceover_script=voiceover_script,
            estimated_duration_sec=int(estimated_duration),
            scene_count=scene_count
        )
    
    def _fetch_story(self, story_id: str) -> str:
        """Fetch raw story from storage (placeholder)."""
        # In production: query database
        return "Placeholder raw story text that would be fetched from database."
    
    def _adapt_text(self, text: str, target_words: int) -> str:
        """
        Adapt text to target word count.
        
        In production, this would call LLM with adaptation prompt.
        """
        words = text.split()
        
        if len(words) <= target_words:
            # Text is already short enough, maybe expand slightly
            return text
        else:
            # Condense text
            condensed = words[:target_words]
            return " ".join(condensed) + "..."
    
    def _create_voiceover_script(self, adapted_text: str) -> str:
        """
        Clean up text for voiceover.
        
        - Remove special characters
        - Fix punctuation for speech
        - Ensure natural flow
        """
        # Simple cleanup (in production, LLM would do this better)
        script = adapted_text.strip()
        
        # Ensure proper sentence endings for TTS
        if not script.endswith(('.', '!', '?')):
            script += '.'
        
        return script
