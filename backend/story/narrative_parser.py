"""
Narrative Parser Module

Parses story text into classic narrative structure.
Identifies hook, buildup, climax, and ending.
"""
from typing import Dict, Any

from .story_schema import NarrativeStructure, ParseNarrativeInput


class NarrativeParser:
    """
    Parses story into narrative structure.
    
    Responsibilities:
    - Analyze story text
    - Identify narrative arc components
    - Extract hook, buildup, climax, ending
    - Return structured NarrativeStructure
    
    Does NOT:
    - Generate images
    - Modify original story
    - Manage pipeline state
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize with optional LLM client for analysis.
        
        Args:
            llm_client: LLM client for narrative analysis
        """
        self.llm_client = llm_client
    
    def parse_structure(self, input_data: Dict[str, Any]) -> NarrativeStructure:
        """
        Parse story text into narrative structure.
        
        Args:
            input_data: Dict with keys:
                - story_text: str
        
        Returns:
            NarrativeStructure with hook, buildup, climax, ending
        
        Flow:
        1. Analyze story text for narrative beats
        2. Identify key turning points
        3. Extract each component
        4. Return structured result
        """
        story_text = input_data["story_text"]
        
        # In real implementation:
        # 1. Send story to LLM with narrative analysis prompt
        # 2. Parse response to extract components
        # 3. Validate all parts are present
        
        # Placeholder: simulate parsing
        return self._simulate_parse(story_text)
    
    def _simulate_parse(self, story_text: str) -> NarrativeStructure:
        """
        Simulate narrative parsing (placeholder for LLM call).
        
        In production, this would use LLM to intelligently identify
        narrative components based on story content.
        """
        sentences = self._split_sentences(story_text)
        
        if len(sentences) < 4:
            # Not enough content, distribute evenly
            return self._simple_distribution(story_text)
        
        # Simple heuristic: divide by position
        total = len(sentences)
        
        # Hook: first 15-20%
        hook_end = max(1, int(total * 0.2))
        hook = " ".join(sentences[:hook_end])
        
        # Buildup: next 30-35%
        buildup_start = hook_end
        buildup_end = buildup_start + max(1, int(total * 0.35))
        buildup = " ".join(sentences[buildup_start:buildup_end])
        
        # Climax: next 25-30%
        climax_start = buildup_end
        climax_end = climax_start + max(1, int(total * 0.3))
        climax = " ".join(sentences[climax_start:climax_end])
        
        # Ending: remaining 20-25%
        ending = " ".join(sentences[climax_end:])
        
        # Ensure all parts have content
        if not ending and climax:
            # Move last sentence to ending
            climax_words = climax.split()
            if len(climax_words) > 5:
                split_point = len(climax_words) // 2
                climax = " ".join(climax_words[:split_point])
                ending = " ".join(climax_words[split_point:])
        
        return NarrativeStructure(
            hook=hook or "Introduction that grabs attention.",
            buildup=buildup or "Story develops and tension builds.",
            climax=climax or "Peak moment of conflict or revelation.",
            ending=ending or "Resolution and conclusion."
        )
    
    def _simple_distribution(self, story_text: str) -> NarrativeStructure:
        """Simple distribution when content is limited."""
        words = story_text.split()
        total = len(words)
        
        if total < 20:
            # Very short text, duplicate for structure
            return NarrativeStructure(
                hook=story_text,
                buildup=story_text,
                climax=story_text,
                ending=story_text
            )
        
        quarter = total // 4
        
        return NarrativeStructure(
            hook=" ".join(words[:quarter]),
            buildup=" ".join(words[quarter:quarter*2]),
            climax=" ".join(words[quarter*2:quarter*3]),
            ending=" ".join(words[quarter*3:])
        )
    
    def _split_sentences(self, text: str) -> list:
        """Split text into sentences."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]
