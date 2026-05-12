"""
Scene Splitter Module

Splits voiceover script into logical scenes.
Each scene represents a semantic unit, NOT visual yet.
"""
import uuid
from typing import Dict, Any, List

from .story_schema import Scene, SplitScenesInput, INVALID_SCENE_SPLIT_ERROR


class SceneSplitter:
    """
    Splits voiceover script into logical scenes.
    
    Responsibilities:
    - Take voiceover script and desired scene count
    - Split by semantic boundaries (sentences, paragraphs)
    - Assign intent and mood to each scene
    - Return list of Scene objects
    
    Does NOT:
    - Generate visual descriptions
    - Create images
    - Manage pipeline state
    
    Note: These are LOGICAL scenes, not visual scenes.
    Visual scenes are created in Block 5 (Scene System).
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize with optional LLM client for intelligent splitting.
        
        Args:
            llm_client: LLM client for semantic analysis
        """
        self.llm_client = llm_client
    
    def split_into_scenes(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Split voiceover script into logical scenes.
        
        Args:
            input_data: Dict with keys:
                - voiceover_script: str
                - scene_count: int
        
        Returns:
            Dict with keys:
                - scenes: List[Scene]
        
        Behavior:
        - Split by semantic boundaries
        - Maintain narrative flow
        - Assign intent/mood to each scene
        - Add transition hints
        
        Fallback:
        - If intelligent split fails, use equal split
        """
        voiceover_script = input_data["voiceover_script"]
        scene_count = input_data["scene_count"]
        
        # Ensure minimum scene count
        scene_count = max(3, min(scene_count, 10))  # 3-10 scenes
        
        # Try intelligent semantic split
        try:
            scenes = self._semantic_split(voiceover_script, scene_count)
        except Exception:
            # Fallback to equal split
            scenes = self._equal_split(voiceover_script, scene_count)
        
        return {"scenes": scenes}
    
    def _semantic_split(self, script: str, scene_count: int) -> List[Scene]:
        """
        Split script by semantic boundaries.
        
        In production, this would:
        1. Use LLM to identify natural break points
        2. Analyze sentence structure
        3. Group by narrative units
        
        For now, simplified implementation.
        """
        # Split into sentences
        sentences = self._split_sentences(script)
        
        if len(sentences) < scene_count:
            # Not enough sentences, use equal split anyway
            raise ValueError("Not enough content for semantic split")
        
        # Group sentences into scenes
        scenes = []
        sentences_per_scene = len(sentences) // scene_count
        
        story_id = str(uuid.uuid4())  # In production, would be from parent story
        
        for i in range(scene_count):
            start_idx = i * sentences_per_scene
            end_idx = start_idx + sentences_per_scene if i < scene_count - 1 else len(sentences)
            
            scene_sentences = sentences[start_idx:end_idx]
            scene_text = " ".join(scene_sentences)
            
            # Extract intent and mood (simplified)
            intent = self._infer_intent(scene_text, i, scene_count)
            mood = self._infer_mood(scene_text, i, scene_count)
            transition = self._infer_transition(i, scene_count)
            
            scene = Scene(
                scene_id=str(uuid.uuid4()),
                story_id=story_id,
                index=i,
                text=scene_text,
                voice_text=scene_text,  # Could be different for TTS
                intent=intent,
                mood=mood,
                transition_hint=transition
            )
            scenes.append(scene)
        
        return scenes
    
    def _equal_split(self, script: str, scene_count: int) -> List[Scene]:
        """
        Fallback: split script into equal parts.
        
        Used when semantic split fails.
        """
        words = script.split()
        words_per_scene = len(words) // scene_count
        
        scenes = []
        story_id = str(uuid.uuid4())
        
        for i in range(scene_count):
            start_idx = i * words_per_scene
            end_idx = start_idx + words_per_scene if i < scene_count - 1 else len(words)
            
            scene_words = words[start_idx:end_idx]
            scene_text = " ".join(scene_words)
            
            intent = self._infer_intent(scene_text, i, scene_count)
            mood = self._infer_mood(scene_text, i, scene_count)
            transition = self._infer_transition(i, scene_count)
            
            scene = Scene(
                scene_id=str(uuid.uuid4()),
                story_id=story_id,
                index=i,
                text=scene_text,
                voice_text=scene_text,
                intent=intent,
                mood=mood,
                transition_hint=transition
            )
            scenes.append(scene)
        
        return scenes
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        # Simple sentence splitting (production would use NLP library)
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]
    
    def _infer_intent(self, text: str, index: int, total: int) -> str:
        """
        Infer scene intent from text and position.
        
        In production, LLM would analyze semantic meaning.
        """
        if index == 0:
            return "hook"
        elif index == total - 1:
            return "resolution"
        elif index < total / 2:
            return "setup"
        else:
            return "development"
    
    def _infer_mood(self, text: str, index: int, total: int) -> str:
        """
        Infer scene mood from text.
        
        In production, LLM would analyze emotional tone.
        """
        # Simplified logic
        if index == 0:
            return "intriguing"
        elif index == total - 1:
            return "satisfying"
        else:
            return "engaging"
    
    def _infer_transition(self, index: int, total: int) -> str:
        """
        Suggest transition type for scene.
        """
        if index == total - 1:
            return "fade_out"
        elif index == 0:
            return "fade_in"
        else:
            return "cut"
