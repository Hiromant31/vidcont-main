"""
Style Extractor Module

Extracts tone, mood, and visual style hints from story text.
Provides style guidance for downstream systems (characters, scenes, visuals).
"""
from typing import Dict, Any

from .story_schema import StyleInfo, ExtractStyleInput


class StyleExtractor:
    """
    Extracts style information from story text.
    
    Responsibilities:
    - Analyze story text for emotional tone
    - Identify mood and atmosphere
    - Extract visual style hints
    - Return structured StyleInfo
    
    Does NOT:
    - Generate images
    - Create visual assets
    - Manage pipeline state
    
    Output is used by:
    - Character System (for character design)
    - Scene System (for visual composition)
    - Image Generation (for style guidance)
    """
    
    # Keyword mappings for style extraction
    TONE_KEYWORDS = {
        "dark": ["horror", "mystery", "thriller", "suspense", "shadow", "fear"],
        "light": ["comedy", "romance", "feel-good", "happy", "bright", "cheerful"],
        "intense": ["action", "drama", "conflict", "battle", "struggle", "tension"],
        "calm": ["slice of life", "peaceful", "serene", "gentle", "quiet"],
        "mysterious": ["mystery", "enigma", "secret", "unknown", "puzzle"],
        "epic": ["adventure", "quest", "journey", "heroic", "grand"],
        "futuristic": ["sci-fi", "future", "technology", "space", "cyber"],
        "magical": ["fantasy", "magic", "wizard", "enchanted", "mythical"]
    }
    
    MOOD_KEYWORDS = {
        "tense": ["danger", "threat", "urgent", "critical", "desperate"],
        "romantic": ["love", "heart", "passion", "affection", "tender"],
        "melancholic": ["sad", "loss", "grief", "lonely", "sorrow"],
        "hopeful": ["hope", "dream", "wish", "believe", "possible"],
        "exciting": ["adventure", "thrill", "rush", "exhilarating", "wild"],
        "contemplative": ["think", "ponder", "reflect", "consider", "wonder"]
    }
    
    VISUAL_STYLE_HINTS = {
        "noir": ["dark", "shadow", "night", "detective", "crime"],
        "pastel": ["soft", "gentle", "dreamy", "light", "delicate"],
        "vibrant": ["colorful", "bright", "bold", "energetic", "dynamic"],
        "minimalist": ["simple", "clean", "sparse", "elegant", "subtle"],
        "cinematic": ["dramatic", "epic", "sweeping", "grand", "spectacular"],
        "intimate": ["close", "personal", "warm", "cozy", "intimate"]
    }
    
    def __init__(self, llm_client=None):
        """
        Initialize with optional LLM client for analysis.
        
        Args:
            llm_client: LLM client for deep style analysis
        """
        self.llm_client = llm_client
    
    def extract_style(self, input_data: Dict[str, Any]) -> StyleInfo:
        """
        Extract style information from story text.
        
        Args:
            input_data: Dict with keys:
                - story_text: str
        
        Returns:
            StyleInfo with tone, mood, visual_style_hint
        
        Flow:
        1. Analyze text for tone keywords
        2. Analyze text for mood indicators
        3. Extract visual style hints
        4. Return structured result
        """
        story_text = input_data["story_text"]
        
        # In real implementation:
        # 1. Send to LLM with style analysis prompt
        # 2. Parse response for tone, mood, visual hints
        # 3. Validate and normalize results
        
        # Placeholder: keyword-based extraction
        return self._extract_by_keywords(story_text)
    
    def _extract_by_keywords(self, text: str) -> StyleInfo:
        """
        Extract style using keyword matching.
        
        In production, LLM would provide more nuanced analysis.
        """
        text_lower = text.lower()
        words = set(text_lower.split())
        
        # Find tone
        tone = self._find_best_match(words, self.TONE_KEYWORDS)
        
        # Find mood
        mood = self._find_best_match(words, self.MOOD_KEYWORDS)
        
        # Find visual style hint
        visual_style = self._find_best_match(words, self.VISUAL_STYLE_HINTS)
        
        # Defaults if nothing matched
        tone = tone or "neutral"
        mood = mood or "engaging"
        visual_style = visual_style or "cinematic"
        
        return StyleInfo(
            tone=tone,
            mood=mood,
            visual_style_hint=visual_style
        )
    
    def _find_best_match(self, words: set, keyword_map: dict) -> str:
        """Find the category with most keyword matches."""
        best_match = None
        best_count = 0
        
        for category, keywords in keyword_map.items():
            matches = len([kw for kw in keywords if kw in words])
            # Also check for multi-word phrases
            text_check = " ".join(words)
            phrase_matches = sum(1 for kw in keywords if kw in text_check)
            
            total_matches = matches + phrase_matches
            
            if total_matches > best_count:
                best_count = total_matches
                best_match = category
        
        return best_match
