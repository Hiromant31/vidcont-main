"""
Script Builder Module

Builds voiceover script from adapted story.
Calculates estimated duration for TTS planning.
"""
import uuid
from typing import Dict, Any

from .story_schema import AdaptedStory


class ScriptBuilder:
    """
    Builds voiceover script from adapted story.
    
    Responsibilities:
    - Take adapted story
    - Format for voiceover delivery
    - Calculate estimated duration
    - Return structured script
    
    Does NOT:
    - Generate images
    - Call TTS (just prepares text)
    - Manage pipeline state
    """
    
    # Speaking rate constants
    WORDS_PER_SECOND = 2.2  # Conservative for clear speech
    PAUSE_BUFFER_SEC = 0.5  # Buffer for natural pauses
    
    def __init__(self):
        """Initialize ScriptBuilder."""
        pass
    
    def build_voiceover_script(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build voiceover script from adapted story.
        
        Args:
            input_data: Dict with keys:
                - adapted_story_id: str
        
        Returns:
            Dict with keys:
                - voiceover_script: str
                - estimated_duration: int (seconds)
        
        Flow:
        1. Fetch AdaptedStory from storage
        2. Format script for TTS (add pause markers if needed)
        3. Calculate precise duration
        4. Return formatted script
        """
        adapted_story_id = input_data["adapted_story_id"]
        
        # In real implementation:
        # 1. Fetch AdaptedStory from database
        # 2. Process script for TTS optimization
        # 3. Add pause markers [pause:0.5s] if system supports it
        # 4. Calculate duration
        
        # Placeholder: simulate fetching and processing
        adapted_story = self._fetch_adapted_story(adapted_story_id)
        
        # Format for voiceover (could add SSML tags or pause markers)
        voiceover_script = self._format_for_tts(adapted_story.voiceover_script)
        
        # Calculate duration
        word_count = len(voiceover_script.split())
        estimated_duration = int((word_count / self.WORDS_PER_SECOND) + self.PAUSE_BUFFER_SEC)
        
        return {
            "voiceover_script": voiceover_script,
            "estimated_duration": estimated_duration
        }
    
    def _fetch_adapted_story(self, adapted_story_id: str) -> AdaptedStory:
        """Fetch adapted story from storage (placeholder)."""
        # In production: query database
        return AdaptedStory(
            story_id="placeholder-id",
            adapted_text="Placeholder adapted text.",
            voiceover_script="Placeholder voiceover script.",
            estimated_duration_sec=60,
            scene_count=5
        )
    
    def _format_for_tts(self, script: str) -> str:
        """
        Format script for TTS engine.
        
        Could add:
        - SSML tags
        - Pause markers
        - Emphasis markers
        - Pronunciation guides
        
        For now, just ensure clean text.
        """
        # Clean up multiple spaces
        import re
        script = re.sub(r'\s+', ' ', script)
        
        # Ensure proper punctuation
        script = script.strip()
        if not script.endswith(('.', '!', '?')):
            script += '.'
        
        return script
